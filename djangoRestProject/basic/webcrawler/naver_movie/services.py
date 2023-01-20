import csv
import urllib
from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from basic.webcrawler.naver_movie.model import ScrapVO
import os.path



class ScrapService(ScrapVO):
    def __init__(self):
        global  driverpath, naver_url, savepath, encoding
        driverpath = r"C:\Users\AIA\PycharmProjects\djangoRestProject\basic\webcrawler\chromedriver.exe" #크롬 드라이버(설정 -> chrome 정보에서 확인한 버전과 맞는 드라이버)
        savepath = r"C:\Users\AIA\PycharmProjects\djangoRestProject\basic\webcrawler\save\navermovie.csv"
        naver_url = "https://movie.naver.com/movie/sdb/rank/rmovie.naver"
        encoding = "UTF-8"

    # 음악 크롤링 깃허브 경로는 flask_program/src/ext(외부 추가 컴포넌트)/scrapper/
    def naver_movie_review(self):
        print('서비스로 들어옴')
        if os.path.isfile(savepath):
            title = pd.read_csv(savepath)
            moviedict = [{"rank": i + 1, "title": j} for i, j in enumerate(title.columns)]
            return moviedict

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
'''if os.path.isfile(savepath):
            title = pd.read_csv(savepath)
            moviedict = [{"rank": i+1, "title": j} for i, j in enumerate(title.columns)]
            return moviedict'''

if __name__ == '__main__':
    ScrapService().naver_movie_review()