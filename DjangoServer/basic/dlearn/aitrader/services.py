import os
import warnings

import numpy as np
import pandas as pd
from prophet import Prophet

from api.path import dir_path

warnings.filterwarnings("ignore")
import pandas_datareader.data as web
from pandas_datareader import data
import yfinance as yf
yf.pdr_override() # TypeError: string indices must be integers 해결법
path = "c:/Windows/Fonts/malgun.ttf"
import platform
from matplotlib import font_manager, rc, pyplot as plt

if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown system... sorry~~~~')
plt.rcParams['axes.unicode_minus'] = False

'''
Date Open     High      Low    Close     Adj Close   Volume
'''



class AiTraderService(object):

    def __init__(self):
        global codes, path, labels, dates, images
        path = dir_path('aitrader')
        dates = {"start":"2019-1-4", "end":"2022-12-30"}
        codes = {"kia":'000270.KS'}
        labels = {'real':'real', 'forecast':'forecast'}
        images = {"kia-close":"kia_close.png"}
        csv_files = {}

    def kospi_predict_by_yahoo(self):
        item = data.get_data_yahoo(codes["kia"], dates["start"], dates["end"])
        print(f" KIA head: {item.head(3)}")
        print(f" KIA tail: {item.tail(3)}")
        item['Close'].plot(figsize=(12,6), grid=True)
        item_trunc = item[:'2021-12-31']
        df = pd.DataFrame({'ds': item_trunc.index, 'y': item_trunc['Close']})
        df.reset_index(inplace=True)
        del df['Date']
        prophet = Prophet(daily_seasonality=True)
        prophet.fit(df)
        future = prophet.make_future_dataframe(periods=61)
        forecast = prophet.predict(future)
        prophet.plot(forecast)
        plt.figure(figsize=(12,6))
        plt.plot(item.index, item['Close'], label=labels['real'])
        plt.plot(forecast['ds'], forecast['yhat'], label=labels['forecast'])
        plt.grid()
        plt.legend()
        plt.savefig(os.path.join(path, "save", images["kia-close"]))

    def samsung_predict(self):
        kospi200_df = pd.read_csv(os.path.join(path, "data", "kospi200.csv"),
                          index_col=0, header=0, encoding="cp949", sep=",")
        print(kospi200_df)
        print(kospi200_df.shape)

        samsung_df = pd.read_csv(os.path.join(path, "data", "samsung.csv"),
                          index_col=0, header=0, encoding="cp949", sep=",")
        print(samsung_df)
        print(samsung_df.shape)

        # kospi200의 거래량
        for i in range(len(kospi200_df.index)):  # 거래량 str -> int 변경
            kospi200_df.iloc[i, 4] = int(kospi200_df.iloc[i, 4].replace(',', ''))
            # 삼성전자의 모든 데이터
        for i in range(len(samsung_df.index)):  # 모든 str -> int 변경
            for j in range(len(samsung_df.iloc[i])):
                samsung_df.iloc[i, j] = int(samsung_df.iloc[i, j].replace(',', ''))

        kospi200_df = kospi200_df.sort_values(['일자'], ascending=[True])
        samsung_df = samsung_df.sort_values(['일자'], ascending=[True])
        print(kospi200_df)
        print(samsung_df)

        kospi200_df = kospi200_df.values
        samsung_df = samsung_df.values
        print(type(kospi200_df), type(samsung_df))
        print(kospi200_df.shape, samsung_df.shape)

        np.save(os.path.join(path, "save", "kospi200.npy"), arr=kospi200_df)
        np.save(os.path.join(path, "save", "samsung.npy"), arr=samsung_df)

if __name__ == '__main__':
    # ai = AiTraderService()
    # ai.samsung_predict()
    label = {'real':'real', 'forecast':'forecast'}
    print(label['real'])


