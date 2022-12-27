import csv
import os

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
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        titles = soup.find_all('td', attrs={'class', 'title'})  #  # 크롤링 하려는 태그
        # all_em = soup.find_all('span', attrs={'class', 'st_on'})
        reviews = [div.br.next_element for div in titles]
        for i, j in enumerate(reviews):
            reviews[i] = j.replace('\n', '')
            reviews[i] = reviews[i].replace('\t', '')
        ratings = [td.em.string for td in titles]
        result = {ratings[i]: reviews[i] for i in range(len(reviews))}
        #df = pd.Series(reviews)
        #df.to_csv(filename, header=None, index=None)
        with open(filename, 'w', encoding=encoding, newline='') as f:
            wr = csv.writer(f, delimiter=',')
            wr.writerows(result.values())
            wr.writerows(result.keys())

            driver.close()


if __name__ == '__main__':
    NaverMovieService().crawling()



