import csv
import os
import time
from collections import defaultdict
from math import log, exp

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from keras.datasets import imdb
from keras.preprocessing.text import Tokenizer

from keras_preprocessing.sequence import pad_sequences
from selenium import webdriver
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB


class KoreanClassifyServices(object):
    def __init__(self):
        pass

    def hook(self):
        ko_str = '이것은 한국어 문장입니다.'
        ja_str = 'これは日本語の文章です。'
        en_str = 'This is English Sentences.'
        x_train = [self.count_codePoint(ko_str),
                   self.count_codePoint(ja_str),
                   self.count_codePoint(en_str)]
        y_train = ['ko', 'ja', 'en']
        clf = GaussianNB()
        clf.fit(x_train, y_train)

        ko_test_str = '안녕하세요'
        ja_test_str = 'こんにちは'
        en_test_str = 'Hello'
        x_test = [self.count_codePoint(ko_test_str),
                    self.count_codePoint(ja_test_str),
                    self.count_codePoint(en_test_str)]
                  #self.count_codePoint(ab)]

        y_test = ['ko', 'ja', 'en']
        y_pred = clf.predict(x_test)
        print(y_pred)
        print(f'정답률 : {accuracy_score(y_test, y_pred)}')
        result = accuracy_score(y_test, y_pred)
        return result


    @staticmethod
    def count_codePoint(str):
        counter = np.zeros(65535) # Unicode 코드 포인트 저장 배열
        for i in range(len(str)):
            print(f"str : {str}")
            code_point = ord(str[i])
            print(f" code_point : {code_point}")
            if code_point > 65535:
                continue
            counter[code_point] += 1
        counter = counter / len(str)
        return counter

    def homonym_classification(self):
        text = """경마장에 있는 말이 뛰고 있다\n
                그의 말이 법이다\n
                가는 말이 고와야 오는 말이 곱다\n"""
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts([text])
        vocab_size = len(tokenizer.word_index) +1
        # 케라스 토크나이저의 정수 인코딩은 인덱스가 1부터 시작하지만,
        # 케라스 원-핫 인코딩에서 배열의 인덱스가 0부터 시작하기 때문에
        # 배열의 크기를 실제 단어 집합의 크기보다 +1로 생성해야하므로 미리 +1 선언
        print(f"단어 집합의 크기 : {vocab_size}")
        print(f"word index : {tokenizer.word_index}")
        sequences = list()
        for line in text.split('\n'): # '\n'을 기준으로 문장 토큰화
            encoded = tokenizer.texts_to_sequences([line])[0]
            for i in range(1, len(encoded)):
                sequence = encoded[:i+1]
                sequences.append(sequence)
        print(f'학습에 사용할 샘플의 갯수: {len(sequences)}')
        print(sequences)

    '''
    시계열 데이터
    : 일련의 순차적으로 정해진 데이터 셋의 집합
    : 시간에 관해 순서가 매겨져 있다는 점과, 연속한 관측치는 서로 상관관계를 갖고 있다
    회귀분석
    : 관찰된 연속형 변수들에 대해 두 변수 사이의 모형을 구한뒤 적합도를 측정해 내는 분석 방법
    '''

if __name__ == '__main__':
    KoreanClassifyServices().hook()

    #ab = "what's your name"
    #KoreanClassifyServices().hook(ab)

    #KoreanClassifyServices().homonym_classification()