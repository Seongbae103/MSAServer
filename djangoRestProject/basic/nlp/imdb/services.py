import csv
import os
import time
from collections import defaultdict
from math import log, exp

import pandas as pd
from bs4 import BeautifulSoup
from keras.datasets import imdb
from keras_preprocessing.sequence import pad_sequences
from selenium import webdriver
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

from admin.path import dir_path
from basic.nlp.imdb.models import ImdbModel


class ImdbServices(object):
    def __init__(self):
        global train_input, train_target, test_input, test_target, train_input2, val_input, train_target2, val_target
        (train_input, train_target), (test_input, test_target) = imdb.load_data(num_words=500)
        train_input2, val_input, train_target2, val_target = train_test_split(train_input, train_target, test_size=0.2, random_state=42)
        self.word_probs = []
    def hook(self):
        model = ImdbModel()
        #self.show_set()
        #self.target_checker()
        dc = self.txt_length()
        model.create(dc['train_seq'], dc['val_seq'])
        model.fit(train_target, val_target)

    def show_set(self):
        print(train_target[:20])
        print(train_input.shape, test_input.shape)
        print(len(train_input[0]))
        print(train_input[0])

    def target_checker(self):
        print(train_target2[:20])
        lengths = np.array([len(x) for x in train_input2])
        print(f"평균값, 중간값 {np.mean(lengths)}, {np.median(lengths)}")
        plt.hist(lengths)
        plt.xlabel('lengths')
        plt.ylabel('frequency') #빈도
        plt.show()

    def txt_length(self):
        train_seq = pad_sequences(train_input, maxlen=100)
        print(train_seq.shape)
        print(train_seq[0])
        print(train_input[0][:-10])
        print(train_seq[5])
        val_seq = pad_sequences(val_input, maxlen=100)
        return {'train_seq':train_seq, 'val_seq':val_seq}


class NaverMovieService(object):
    def __init__(self):
        global url, filename, driverpath, encoding, review_train, k
        url = "http://movie.naver.com/movie/point/af/list.naver?&page=1"
        filename = os.path.join(dir_path("imdb"), "../imdb/data", "naver_movie_review_corpus.csv")
        #driverpath = os.path.join(os.getcwd(), "webcrawler", "chromedriver.exe") #os.getcwd()는 작동시키는 manage
        driverpath = os.path.join(dir_path("webcrawler"), "chromedriver.exe")
        review_train = os.path.join(dir_path("imdb"), "../imdb/data", "review_train.csv")
        encoding = 'UTF-8'
        k = 0.5
        self.word_prob = []

    def process(self, new_review):
        service = NaverMovieService()
        service.model_fit()
        result = service.classify(new_review)
        return result

    def crawling(self):
        if not os.path.exists(review_train):   # filename -> review_train
            review_data = []
            driver = webdriver.Chrome(driverpath)
            for page in range(1, 2):
                driver.get(url + str(page))
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                all_tds = soup.find_all('td', attrs={'class', 'title'})
                for review in all_tds:
                    need_reviews_cnt = 1000
                    sentence = review.find("a", {"class": "report"}).get("onclick").split("', '")[2]
                    if sentence != "":  # 리뷰 내용이 비어있다면 데이터를 사용하지 않음
                        score = review.find("em").get_text()
                        review_data.append([sentence, int(score)])
            time.sleep(1)  # 다음 페이지를 조회하기 전 1초 시간 차를 두기
            with open(filename, 'w', newline='', encoding=encoding) as f:
                wr = csv.writer(f)
                wr.writerows(review_data)
            driver.close()

        data = pd.read_csv(filename, header=None)
        data.columns = ['review', 'score']
        result = [print(f"{i + 1}. {data['score'][i]}\n{data['review'][i]}\n") for i in range(len(data))]
        return result

    def load_corpus(self):
        corpus = pd.read_table(review_train, sep=",", encoding=encoding)
        corpus = np.array(corpus)
        return corpus

    def count_words(self, train_X):
        counts = defaultdict(lambda : [0, 0])
        for doc, point in train_X:
            if self.isNumber(doc) is False:
                words = doc.split()
                for word in words:
                    counts[word][0 if point > 3.5 else 1] += 1
            '''else:
                print('리뷰의 평점이 실수(float)로 되어 있지 않다')'''
        return counts

    def isNumber(self, param):
        try:
            float(param)
            return True
        except ValueError:
            return False

    def probability(self, word_probs, doc):
        docwords = doc.split() # AttributeError: 'dict' object has no attribute 'split'
        log_prob_if_class0 = log_prob_if_class1 = 0.0
        for word, prob_if_class0, prob_if_class1 in word_probs:
            if word in docwords:
                log_prob_if_class0 += log(prob_if_class0)
                log_prob_if_class1 += log(prob_if_class1)
            else:
                log_prob_if_class0 += log(1.0 - prob_if_class0)
                log_prob_if_class1 += log(1.0 - prob_if_class1)
        prob_if_class0 = exp(log_prob_if_class0)
        prob_if_class1 = exp(log_prob_if_class1)
        return prob_if_class0 / (prob_if_class0 + prob_if_class1)

    def word_probabilities(self, counts, n_class0, n_class1, k):
        return [(w,
                 (class0 + k) / (n_class0 + 2 * k),
                 (class1 + k) / (n_class1 + 2 * k))
                 for w, (class0, class1) in counts.items()]
    def classify(self, doc):
        return self.probability(word_probs=self.word_probs, doc=doc)

    def model_fit(self):
        train_X = self.load_corpus()
        '''
        '재미있다':[1,0]
        '재미없다':[0,1]
        '''
        num_class0 = len([1 for _, point in train_X if point > 3.5])
        num_class1 = len(train_X) - num_class0
        word_counts = self.count_words(train_X)
        self.word_probs = self.word_probabilities(word_counts, num_class0, num_class1, k)



if __name__ == '__main__':
    #service = NaverMovieService()
    result = NaverMovieService().process("왜 지금은 되는데 이유라도 알자")
    print(f"긍정:{result}")



