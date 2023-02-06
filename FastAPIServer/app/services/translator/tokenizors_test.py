import pandas as pd
import urllib.request

from tokenizers.implementations import BertWordPieceTokenizer, ByteLevelBPETokenizer, CharBPETokenizer, \
    SentencePieceBPETokenizer

"""
구글이 공개한 딥 러닝 모델 BERT에는 WordPiece Tokenizer가 사용되었습니다. 
허깅페이스는 해당 토크나이저를 직접 구현하여 tokenizers라는 패키지를 통해 
버트워드피스토크나이저(BertWordPieceTokenizer)를 제공합니다.

여기서는 네이버 영화 리뷰 데이터를 해당 토크나이저에 학습시키고, 
이로부터 서브워드의 단어 집합(Vocabulary)을 얻습니다. 
그리고 임의의 문장에 대해서 학습된 토크나이저를 사용하여 토큰화를 진행합니다. 
우선 네이버 영화 리뷰 데이터를 로드합니다.

"""

"""
딥러닝을 이용한 자연어 처리 입문
소스코드 출처 : https://wikidocs.net/24996
"""
class TokenizersTest:
    def __init__(self):
        pass

    def exec(self):
        urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings.txt",
                                   filename="ratings.txt")
        naver_df = pd.read_table('ratings.txt')
        naver_df = naver_df.dropna(how='any')
        with open('naver_review.txt', 'w', encoding='utf8') as f:
            f.write('\n'.join(naver_df['document']))
        tokenizer = BertWordPieceTokenizer(lowercase=False)
        """
        lowercase : 대소문자를 구분 여부. True일 경우 구분하지 않음.
        strip_accents : True일 경우 악센트 제거.
        ex) é → e, ô → o
        """

        data_file = 'naver_review.txt'
        vocab_size = 30000
        limit_alphabet = 6000
        min_frequency = 5
        # 버트워드피스토크나이저를 설정합니다.
        tokenizer.train(files=data_file,
                        vocab_size=vocab_size,
                        limit_alphabet=limit_alphabet,
                        min_frequency=min_frequency)
        """
        files : 단어 집합을 얻기 위해 학습할 데이터
        vocab_size : 단어 집합의 크기
        limit_alphabet : 병합 전의 초기 토큰의 허용 개수.
        min_frequency : 최소 해당 횟수만큼 등장한 쌍(pair)의 경우에만 병합 대상이 된다.
        """
        # 네이버 영화 리뷰 데이터를 학습하여 단어 집합을 얻어봅시다.
        data_file = 'naver_review.txt'
        vocab_size = 30000
        limit_alphabet = 6000
        min_frequency = 5

        tokenizer.train(files=data_file,
                        vocab_size=vocab_size,
                        limit_alphabet=limit_alphabet,
                        min_frequency=min_frequency)

        # vocab 저장
        tokenizer.save_model('./save')
        # vocab 로드
        df = pd.read_fwf('./save/vocab.txt', header=None)
        print(" ********* vocab.txt ********* ")
        print(df)
        print(" *************************** ")
        """
        총 30,000개의 단어가 존재합니다. 
        이는 단어 집합의 크기를 30,000으로 지정하였기 때문입니다. 
        실제 토큰화를 수행해봅시다.
        """
        encoded = tokenizer.encode('아 배고픈데 짜장면먹고싶다')
        print('토큰화 결과 :', encoded.tokens)
        print('정수 인코딩 :', encoded.ids)
        print('디코딩 :', tokenizer.decode(encoded.ids))
        """
        .ids는 실질적인 딥 러닝 모델의 입력으로 사용되는 정수 인코딩 결과를 출력합니다. 
        tokens는 해당 토크나이저가 어떻게 토큰화를 진행했는지를 보여줍니다. 
        decode()는 정수 시퀀스를 문자열로 복원합니다.
        """
        encoded = tokenizer.encode('커피 한잔의 여유를 즐기다')
        print('토큰화 결과 :', encoded.tokens)
        print('정수 인코딩 :', encoded.ids)
        print('디코딩 :', tokenizer.decode(encoded.ids))
        """
        이 외 ByteLevelBPETokenizer, CharBPETokenizer, SentencePieceBPETokenizer 등이 존재하며 선택에 따라서 사용할 수 있습니다.

        BertWordPieceTokenizer : BERT에서 사용된 워드피스 토크나이저(WordPiece Tokenizer)
        CharBPETokenizer : 오리지널 BPE
        ByteLevelBPETokenizer : BPE의 바이트 레벨 버전
        SentencePieceBPETokenizer : 앞서 본 패키지 센텐스피스(SentencePiece)와 호환되는 BPE 구현체
        """

        tokenizer = SentencePieceBPETokenizer()
        tokenizer.train('naver_review.txt', vocab_size=10000, min_frequency=5)

        encoded = tokenizer.encode("이 영화는 정말 재미있습니다.")
        print(encoded.tokens)

if __name__ == '__main__':
    TokenizersTest().exec()