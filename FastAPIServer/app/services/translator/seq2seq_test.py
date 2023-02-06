import os
import zipfile
import pandas as pd
import urllib3
from keras_preprocessing.sequence import pad_sequences

from keras.layers import Input, LSTM, Dense
from keras.models import Model
import numpy as np
"""
딥러닝을 이용한 자연어 처리 입문
소스코드 출처 : https://wikidocs.net/24996
"""
class Seq2seqTest:
    def __init__(self):
        pass
    def exec(self):
        http = urllib3.PoolManager()
        url = 'https://www.manythings.org/anki/fra-eng.zip'
        filename = 'fra-eng.zip'
        path = os.getcwd()
        zipfilename = os.path.join(path, filename)
        #with http.request('GET', url, preload_content=False) as r, open(zipfilename, 'wb') as out_file:
        #    shutil.copyfileobj(r, out_file)

        with zipfile.ZipFile(zipfilename, 'r') as zip_ref:
            zip_ref.extractall(path)

        lines = pd.read_csv('fra.txt', names=['src', 'tar', 'lic'], sep='\t')
        del lines['lic']
        print('전체 샘플의 개수 :', len(lines))

        lines = lines.loc[:, 'src':'tar']
        lines = lines[0:60000]  # 6만개만 저장
        lines.sample(10)
        """
        해당 데이터는 약 19만 2천개의 병렬 문장 샘플로 구성되어있지만 
        여기서는 간단히 60,000개의 샘플만 가지고 기계 번역기를 구축해보도록 하겠습니다. 
        우선 전체 데이터 중 60,000개의 샘플만 저장하고 
        현재 데이터가 어떤 구성이 되었는지 확인해보겠습니다.
        """
        lines.tar = lines.tar.apply(lambda x: '\t ' + x + ' \n')
        lines.sample(10)
        """
        랜덤으로 10개의 샘플을 선택하여 출력하였습니다. 
        프랑스어 데이터에서 시작 심볼과 종료 심볼이 추가된 것을 볼 수 있습니다. 
        문자 집합을 생성해보겠습니다. 
        단어 집합이 아니라 문자 집합이라고 하는 이유는 토큰 단위가 단어가 아니라 
        문자이기 때문입니다.
        """
        # 문자 집합 구축
        src_vocab = set()
        for line in lines.src:  # 1줄씩 읽음
            for char in line:  # 1개의 문자씩 읽음
                src_vocab.add(char)

        tar_vocab = set()
        for line in lines.tar:
            for char in line:
                tar_vocab.add(char)

        src_vocab_size = len(src_vocab) + 1
        tar_vocab_size = len(tar_vocab) + 1
        print('source 문장의 char 집합 :', src_vocab_size)
        print('target 문장의 char 집합 :', tar_vocab_size)

        src_vocab = sorted(list(src_vocab))
        tar_vocab = sorted(list(tar_vocab))
        print(src_vocab[45:75])
        print(tar_vocab[45:75])
        """
        문자 집합에 문자 단위로 저장된 것을 확인할 수 있습니다. 각 문자에 인덱스를 부여하겠습니다.
        """
        src_to_index = dict([(word, i + 1) for i, word in enumerate(src_vocab)])
        tar_to_index = dict([(word, i + 1) for i, word in enumerate(tar_vocab)])
        print(src_to_index)
        print(tar_to_index)

        """
        인덱스가 부여된 문자 집합으로부터 갖고있는 훈련 데이터에 정수 인코딩을 수행합니다. 
        우선 인코더의 입력이 될 영어 문장 샘플에 대해서 정수 인코딩을 수행해보고, 
        5개의 샘플을 출력해봅시다.
        """
        encoder_input = []

        # 1개의 문장
        for line in lines.src:
            encoded_line = []
            # 각 줄에서 1개의 char
            for char in line:
                # 각 char을 정수로 변환
                encoded_line.append(src_to_index[char])
            encoder_input.append(encoded_line)
        print('source 문장의 정수 인코딩 :', encoder_input[:5])
        """
        정수 인코딩이 수행된 것을 볼 수 있습니다. 
        디코더의 입력이 될 프랑스어 데이터에 대해서 
        정수 인코딩을 수행해보겠습니다.
        """
        decoder_input = []
        for line in lines.tar:
            encoded_line = []
            for char in line:
                encoded_line.append(tar_to_index[char])
            decoder_input.append(encoded_line)
        print('target 문장의 정수 인코딩 :', decoder_input[:5])
        """
        정상적으로 정수 인코딩이 수행된 것을 볼 수 있습니다. 
        아직 정수 인코딩을 수행해야 할 데이터가 하나 더 남았습니다. 
        디코더의 예측값과 비교하기 위한 실제값이 필요합니다. 
        그런데 이 실제값에는 시작 심볼에 해당되는 <sos>가 있을 필요가 없습니다. 
        이해가 되지 않는다면 이전 페이지의 그림으로 돌아가 Dense와 Softmax 위에 있는 
        단어들을 다시 보시기 바랍니다. 
        그래서 이번에는 정수 인코딩 과정에서 <sos>를 제거합니다. 
        즉, 모든 프랑스어 문장의 맨 앞에 붙어있는 '\t'를 제거하도록 합니다.
        """
        decoder_target = []
        for line in lines.tar:
            timestep = 0
            encoded_line = []
            for char in line:
                if timestep > 0:
                    encoded_line.append(tar_to_index[char])
                timestep = timestep + 1
            decoder_target.append(encoded_line)
        print('target 문장 레이블의 정수 인코딩 :', decoder_target[:5])
        """
        앞서 먼저 만들었던 디코더의 입력값에 해당되는 decoder_input 데이터와 비교하면 decoder_input에서는 모든 문장의 앞에 붙어있던 숫자 1이 decoder_target에서는 제거된 것을 볼 수 있습니다. '\t'가 인덱스가 1이므로 정상적으로 제거된 것입니다. 모든 데이터에 대해서 정수 인덱스로 변경하였으니 패딩 작업을 수행합니다. 패딩을 위해서 영어 문장과 프랑스어 문장 각각에 대해서 가장 길이가 긴 샘플의 길이를 확인합니다.
        """
        max_src_len = max([len(line) for line in lines.src])
        max_tar_len = max([len(line) for line in lines.tar])
        print('source 문장의 최대 길이 :', max_src_len)
        print('target 문장의 최대 길이 :', max_tar_len)
        """
        각각 23와 76의 길이를 가집니다. 
        가장 긴 샘플의 길이에 맞춰서 영어 데이터의 샘플은 전부 길이가 23이 되도록 패딩하고, 프랑스어 데이터의 샘플은 전부 길이가 76이 되도록 패딩합니다.
        """
        encoder_input = pad_sequences(encoder_input, maxlen=max_src_len, padding='post')
        decoder_input = pad_sequences(decoder_input, maxlen=max_tar_len, padding='post')
        decoder_target = pad_sequences(decoder_target, maxlen=max_tar_len, padding='post')
        encoder_inputs = Input(shape=(None, src_vocab_size))
        encoder_lstm = LSTM(units=256, return_state=True)

        # encoder_outputs은 여기서는 불필요
        encoder_outputs, state_h, state_c = encoder_lstm(encoder_inputs)

        # LSTM은 바닐라 RNN과는 달리 상태가 두 개. 은닉 상태와 셀 상태.
        encoder_states = [state_h, state_c]
        decoder_inputs = Input(shape=(None, tar_vocab_size))
        decoder_lstm = LSTM(units=256, return_sequences=True, return_state=True)

        # 디코더에게 인코더의 은닉 상태, 셀 상태를 전달.
        decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)

        decoder_softmax_layer = Dense(tar_vocab_size, activation='softmax')
        decoder_outputs = decoder_softmax_layer(decoder_outputs)

        model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
        model.compile(optimizer="rmsprop", loss="categorical_crossentropy")

        model.fit(x=[encoder_input, decoder_input], y=decoder_target, batch_size=64, epochs=40, validation_split=0.2)

        encoder_model = Model(inputs=encoder_inputs, outputs=encoder_states)

        # 이전 시점의 상태들을 저장하는 텐서
        decoder_state_input_h = Input(shape=(256,))
        decoder_state_input_c = Input(shape=(256,))
        decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

        # 문장의 다음 단어를 예측하기 위해서 초기 상태(initial_state)를 이전 시점의 상태로 사용.
        # 뒤의 함수 decode_sequence()에 동작을 구현 예정
        decoder_outputs, state_h, state_c = decoder_lstm(decoder_inputs, initial_state=decoder_states_inputs)

        # 훈련 과정에서와 달리 LSTM의 리턴하는 은닉 상태와 셀 상태를 버리지 않음.
        decoder_states = [state_h, state_c]
        decoder_outputs = decoder_softmax_layer(decoder_outputs)
        decoder_model = Model(inputs=[decoder_inputs] + decoder_states_inputs,
                              outputs=[decoder_outputs] + decoder_states)

        index_to_src = dict((i, char) for char, i in src_to_index.items())
        index_to_tar = dict((i, char) for char, i in tar_to_index.items())

        for seq_index in [3, 50, 100, 300, 1001]:  # 입력 문장의 인덱스
            input_seq = encoder_input[seq_index:seq_index + 1]
            decoded_sentence = self.decode_sequence(input_seq, encoder_model, tar_vocab_size,
                        tar_to_index, decoder_model, index_to_tar, max_tar_len)
            print(35 * "-")
            print('입력 문장:', lines.src[seq_index])
            print('정답 문장:', lines.tar[seq_index][2:len(lines.tar[seq_index]) - 1])  # '\t'와 '\n'을 빼고 출력
            print('번역 문장:', decoded_sentence[1:len(decoded_sentence) - 1])  # '\n'을 빼고 출력

    def decode_sequence(self, input_seq, encoder_model, tar_vocab_size,
                        tar_to_index, decoder_model, index_to_tar, max_tar_len):
        # 입력으로부터 인코더의 상태를 얻음
        states_value = encoder_model.predict(input_seq)

        # <SOS>에 해당하는 원-핫 벡터 생성
        target_seq = np.zeros((1, 1, tar_vocab_size))
        target_seq[0, 0, tar_to_index['\t']] = 1.

        stop_condition = False
        decoded_sentence = ""

        # stop_condition이 True가 될 때까지 루프 반복
        while not stop_condition:
            # 이점 시점의 상태 states_value를 현 시점의 초기 상태로 사용
            output_tokens, h, c = decoder_model.predict([target_seq] + states_value)

            # 예측 결과를 문자로 변환
            sampled_token_index = np.argmax(output_tokens[0, -1, :])
            sampled_char = index_to_tar[sampled_token_index]

            # 현재 시점의 예측 문자를 예측 문장에 추가
            decoded_sentence += sampled_char

            # <eos>에 도달하거나 최대 길이를 넘으면 중단.
            if (sampled_char == '\n' or
                    len(decoded_sentence) > max_tar_len):
                stop_condition = True

            # 현재 시점의 예측 결과를 다음 시점의 입력으로 사용하기 위해 저장
            target_seq = np.zeros((1, 1, tar_vocab_size))
            target_seq[0, 0, sampled_token_index] = 1.

            # 현재 시점의 상태를 다음 시점의 상태로 사용하기 위해 저장
            states_value = [h, c]

        return decoded_sentence


if __name__ == '__main__':
    Seq2seqTest().exec()