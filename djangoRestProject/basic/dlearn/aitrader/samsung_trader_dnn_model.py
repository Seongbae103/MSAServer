import os
import sys

import numpy as np
import pandas as pd
from keras.callbacks import EarlyStopping
from keras.layers import Dense
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from admin.path import dir_path


class SamsungTraderDnnModel(object):
    def __int__(self):
        pass

    def hook(self):
        self.save_npy()


    def save_npy(self):
        kospidf = pd.read_csv("./data/코스피200.csv", index_col=0, header=0, encoding='utf-8', sep=',').dropna()

        samsungdf = pd.read_csv("./data/삼성전자.csv", index_col=0, header=0, encoding='utf-8', sep=',').dropna()
        for i in range(len(kospidf.index)):
                kospidf.iloc[i, 4] = str(kospidf.iloc[i, 4])
                kospidf.iloc[i, 4] = kospidf.iloc[i, 4].replace('M', '')
                kospidf.iloc[i, 4] = kospidf.iloc[i, 4].replace('B', '')
                kospidf.iloc[i, 4] = kospidf.iloc[i, 4].replace('K', '')
                kospidf.iloc[i, 4] = int(kospidf.iloc[i, 4].replace('.', ''))

        print(f" sam {samsungdf}")
        for i in range(len(samsungdf.index)):
            for j in range(len(samsungdf.iloc[i])):
                samsungdf.iloc[i, j] = str(samsungdf.iloc[i, j])
                samsungdf.iloc[i, j] = samsungdf.iloc[i, j].replace('.', '')  # loc: 데이터 프레임에 label값으로 접근 / iloc: 데이터 프레임에 index값으로 접근
                samsungdf.iloc[i, j] = samsungdf.iloc[i, j].replace('M', '')
                samsungdf.iloc[i, j] = samsungdf.iloc[i, j].replace('K', '')
                samsungdf.iloc[i, j] = samsungdf.iloc[i, j].replace(',', '')
                samsungdf.iloc[i, j] = int(samsungdf.iloc[i, j].replace('%', ''))

        print(f" sam {samsungdf}")
        print(f" null sam {samsungdf.isnull().sum()}")
        print(f" ko {kospidf}")
        print(f" null ko {kospidf.isnull().sum()}")
        samsungdf = samsungdf.dropna()
        samsungdf = samsungdf.drop(["변동 %"], axis=1)
        kospidf = kospidf.dropna()
        kospidf = kospidf.drop(["변동 %"], axis=1)
        print(f" sam {samsungdf.shape}")
        print(f" ko {kospidf.shape}")
        kospidf = kospidf.sort_values(['날짜'], ascending=[True])
        samsungdf = samsungdf.sort_values(['날짜'], ascending=[True])
        kospidf = kospidf.values
        samsungdf = samsungdf.values


        np.save('./data/kospi200.npy', arr=kospidf)
        np.save('./data/samsung.npy', arr=samsungdf)

    def split_xy5(self, dataset, time_steps, y_column):
        x, y = [], []
        samsung = np.load('./data/samsung.npy', allow_pickle=True)
        dataset = samsung
        time_steps = 5
        y_column = 1
        for i in range(len(dataset)):
            x_end_number = i + time_steps
            y_end_number = x_end_number + y_column

            if y_end_number > len(dataset):
                break
            tmp_x = dataset[i:x_end_number, :]
            tmp_y = dataset[x_end_number:y_end_number, 0]
            x.append(tmp_x)
            y.append(tmp_y)
        return np.array(x), np.array(y)

    def split_xy(self):
        samsung = np.load('./data/samsung.npy', allow_pickle=True)
        x, y = self.split_xy5(samsung, 5, 1)
        #print(x[0, :], '\n', y[0])
        #print(x.shape)
        #print(y.shape)
        return x, y

    def preprocess(self):
        x, y = self.split_xy()
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.3)

        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1] * x_train.shape[2]))
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1] * x_test.shape[2]))  #x_train과 x_test의 차원 축소

        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        return self.x_train, self.x_test, self.y_train, self.y_test

    def create_model(self):
        x_train = self.x_train
        path = dir_path('aitrader')
        scaler = StandardScaler()
        scaler.fit(x_train)
        x_train_scaled = scaler.transform(x_train)
        x_test_scaled = scaler.transform(self.x_test)
        model = Sequential()
        model.add(Dense(64, input_shape=(25,))) # add
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mse', optimizer='adam', metrics=['mse']) # compile

        early_stopping = EarlyStopping(patience=20)
        x_train_scaled = x_train_scaled.astype(np.float32)
        x_test_scaled = x_test_scaled.astype(np.float32)
        self.y_train = self.y_train.astype(np.float32)
        self.y_test = self.y_test.astype(np.float32)
        np.set_printoptions(threshold=sys.maxsize)
        ######################
        model.fit(x_train_scaled, self.y_train, validation_split=0.2, verbose=1, batch_size=1, epochs=100, callbacks=[early_stopping]) # fit : batch_size, epochs

        loss, mse = model.evaluate(x_test_scaled, self.y_test, batch_size=1) #test(반복x)
        print('loss : ', loss)
        print('mse : ', mse)
        y_pred = model.predict(x_test_scaled)

        for i in range(5):
            print('종가 : ', self.y_test[i], '/예측가 : ', y_pred[i])
        file_name = os.path.join(path, "save", "samsung_stock_dnn_model.h5")
        print(f"저장경로: {file_name}")
        model.save(file_name)




if __name__ == '__main__':
    SamsungTraderDnnModel().hook()