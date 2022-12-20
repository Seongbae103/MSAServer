import csv
import urllib
from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from basic.webcrawler.Model import ScrapVO
import os.path



class ScrapService(ScrapVO):
    def __init__(self):
        global  driverpath, naver_url, savepath, encoding
        driverpath = r"C:\Users\AIA\PycharmProjects\djangoRestProject\basic\webcrawler\chromedriver.exe" #크롬 드라이버(설정 -> chrome 정보에서 확인한 버전과 맞는 드라이버)
        savepath = r"C:\Users\AIA\PycharmProjects\djangoRestProject\basic\webcrawler\save\navermovie.csv"
        naver_url = "https://movie.naver.com/movie/sdb/rank/rmovie.naver"
        encoding = "UTF-8"

    def bugs_music(self, arg): # 기본 크롤링
        soup = BeautifulSoup(urlopen(arg.domain + arg.query_string), 'lxml')
        title = {"class": arg.class_names[0]}
        artist = {"class": arg.class_names[1]}
        titles = soup.find_all(name=arg.tag_name, attrs=title)
        titles = [i.find('a').text for i in titles]
        artists = soup.find_all(name=arg.tag_name, attrs=artist)
        artists = [i.find('a').text for i in artists]
        [print(f"{i}위 {j} : {k}")  # 디버깅
         for i, j, k in zip(range(1, len(titles)), titles, artists)]
        diction = {}  # dict 로 변환
        for i, j in enumerate(titles):
            diction[j] = artists[i]
        arg.diction = diction
        arg.dict_to_dataframe()
        arg.dataframe_to_csv()  # csv파일로 저장

    def melon_music(arg): #beautifulSoup 기본 크롤링
        soup = BeautifulSoup(
            urlopen(urllib.request.Request(arg.domain + arg.query_string, headers={'User-Agent': 'My User Agent 1.0'})),
            "lxml")
        title = {"class": arg.class_names[0]}
        artist = {"class": arg.class_names[1]}
        titles = soup.find_all(name=arg.tag_name, attrs=title)
        titles = [i.find('a').text for i in titles]
        artists = soup.find_all(name=arg.tag_name, attrs=artist)
        artists = [i.find('a').text for i in artists]
        [print(f"{i}위 {j} : {k}")  # 디버깅
         for i, j, k in zip(range(1, len(titles)), titles, artists)]
        diction = {}  # dict 로 변환
        for i, j in enumerate(titles):
            diction[j] = artists[i]
        arg.diction = diction
        arg.dict_to_dataframe()
        arg.dataframe_to_csv()  # csv파일로 저장

    def naver_movie_review(self):
        if os.path.isfile(savepath):
            df = pd.read_csv(savepath)
            return df.columns[0]

        else:
            driver = webdriver.Chrome(driverpath)
            driver.get(naver_url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            all_divs = soup.find_all('div', attrs={'class', 'tit3'})  # 크롤링 하려는 태그
            products = [[div.a.string for div in all_divs]]
            with open(savepath, 'w', newline='', encoding=encoding) as f:
                wr = csv.writer(f)
                wr.writerows(products)
            driver.close()
            return products[0][0]

if __name__ == '__main__':
    ScrapService().naver_movie_review()