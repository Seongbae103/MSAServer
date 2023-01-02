import os
import warnings
import pandas as pd
from prophet import Prophet

from admin.path import dir_path

warnings.filterwarnings("ignore")
import pandas_datareader.data as web # restful에서 데이터 저장되는 프로퍼티는 전부 데이터로 통합
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

'''Open     High      Low    Close     Adj Close   Volume(거래량)   Date'''

class AiTraderService(object):
    def __init__(self):
        global start_date, end_date, item_code
        start_date = "2018-1-4"
        end_date = "2021-9-30"
        item_code = '000270.KS'

    def hook(self):
        item = data.get_data_yahoo(item_code, start_date, end_date)
        print(f" KIA head : {item.head(3)}")
        print(f" KIA tail : {item.tail(3)}")
        item['Close'].plot(figsize=(12, 6), grid=True)
        item_trunc = item[:"2021-12-31"]
        df = pd.DataFrame({'ds': item_trunc.index, 'y' : item_trunc['Close']})
        df.reset_index(inplace=True)
        del df['Date']
        prophet = Prophet(daily_seasonality=True)
        prophet.fit(df)
        future = prophet.make_future_dataframe(periods=61)
        forecast = prophet.predict(future)
        prophet.plot(forecast)
        plt.figure(figsize=(12, 6))
        plt.plot(item.index, item['Close'], label='forecast')
        plt.grid()
        plt.legend()
        path = dir_path('aitrader')
        plt.savefig(os.path.join(path, 'kia_close.png'))


if __name__ == '__main__':
    AiTraderService().hook()

