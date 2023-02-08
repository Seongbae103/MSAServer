#  개체명 인식 모듈 생성
import tensorflow as tf
import numpy as np
from keras.models import load_model
from keras import preprocessing

from app.trains.chatbot.food_preprocess import Preprocess


# 개체명 인식 모델 모듈
class NerModel:
    def __init__(self, model_name, proprocess):

        # BIO 태그 클래스별 레이블
        self.index_to_ner = {1: '0', 2:'B_DT', 3:'B_FOOD', 4: 'I', 5:'B_OG', 6:'B_PS',
                             7: 'B_LC', 8:'NNP', 9:'B_TI', 0:'PAD'}

        # 의도 분류 모델 불러오기
        self.model = load_model(model_name)

        # 챗봇 Preprocess 객체
        self.p = proprocess

    # 개체명 클래스 예측 - 질문(query)를 전달받는다.
    def predict(self, query):
        ## 형태소 분석 - 문장의 단어를 나눠 태깅 처리한다.
        pos = self.p.pos(query)

        # 각 단어마다의 품사 정보 가져오기 (불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag=True)
        ## 가져온 단어에 대하여 인덱싱
        sequences = [self.p.get_wordidx_sequence(keywords)]

        # 패딩 처리 - 기존 단어 외의 나머지 40이하의 범위는 전부 0으로 처리
        max_len = 40
        padded_seqs = preprocessing.sequence.pad_sequences(sequences,
                                                           padding='post', value=0, maxlen=max_len)

        # 키워드별 개체명 예측
        predict = self.model.predict(np.array([padded_seqs[0]]))
        predict_class = tf.math.argmax(predict, axis=-1)   # argmax()를 통해 가장 높은 값의 인덱스를 반환

        # 예측된 인덱스를 index_to_ner을 통해 BIO형식으로 바꿔준다.
        tags = [self.index_to_ner[i] for i in predict_class.numpy()[0]]
        # 키워드와 예측된 태그를 압축하여 리스트화 시킨 후 반환
        return list(zip(keywords, tags))

    def predict_tags(self, query):
        # 형태소 분석
        pos = self.p.pos(query)

        # 문장 내 키워드 추출(불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        # 패딩 처리
        max_len = 40
        padded_seqs = preprocessing.sequence.pad_sequences(sequences,
                                                           padding='post', value=0, maxlen=max_len)

        predict = self.model.predict(np.array([padded_seqs[0]]))
        predict_class = tf.math.argmax(predict, axis=-1)

        tags = []
        for tag_idx in predict_class.numpy()[0]:
            if tag_idx == 1: continue       # 만약 인덱스 태그가 1('O')이라면 건너뛰고,
            tags.append(self.index_to_ner[tag_idx]) ## 예측 결과 태그를 tags에 따로 저장

        if len(tags) == 0:  ## 태그의 길이가 0이라면 None을 반환  (*여기 줄맞춤 불확실)
            return None

        return tags

    def ner_test(self):
        p = Preprocess(word2index_dic="/Users/dianakang/NLP/train_tools/dict/chatbot_dict.bin",
                       userdic="/Users/dianakang/NLP/utils/user_dic.tsv")

        ner = NerModel(model_name="/Users/dianakang/NLP/models/ner/ner_model.h5", proprocess=p)

        query = "오늘 오전 13시 3분에 탕수육 주문하고 싶어요"

        predicts = ner.predict(query)

        print(predicts)