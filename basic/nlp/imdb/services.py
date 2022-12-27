import csv
import os
import time

import pandas as pd
from bs4 import BeautifulSoup
from keras.datasets import imdb
from keras_preprocessing.sequence import pad_sequences
from selenium import webdriver
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from basic.nlp.imdb.models import ImdbModel


class ImdbServices(object):
    def __init__(self):
        global train_input, train_target, test_input, test_target, train_input2, val_input, train_target2, val_target
        (train_input, train_target), (test_input, test_target) = imdb.load_data(num_words=500)
        train_input2, val_input, train_target2, val_target = train_test_split(train_input, train_target, test_size=0.2, random_state=42)

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
        global url, filename, driver, encoding
        url = "http://movie.naver.com/movie/point/af/list.naver?&page=1"
        filename = r"C:\Users\AIA\PycharmProjects\djangoRestProject\basic\nlp\imdb\naver_movie_review_corpus.csv"
        driver = webdriver.Chrome(r"C:\Users\AIA\PycharmProjects\djangoRestProject\basic\webcrawler\chromedriver.exe")
        encoding = 'UTF-8'
    def crawling(self):
        if not os.path.exists(filename):
            review_data = []
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


if __name__ == '__main__':
    NaverMovieService().crawling()



