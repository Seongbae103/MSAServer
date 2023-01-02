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
        global path
        path = dir_path('aitrader')


    def split_xy5(self, dataset, time_steps, y_column):
        x, y = [], []
        samsung = np.load('./data/samsung.npy', allow_pickle=True)
        dataset = samsung
        time_steps = 5
        y_column =1
        for i in range(len(dataset)):
            x_end_number = i + time_steps
            y_end_number = x_end_number + y_column

            if y_end_number > len(dataset):
                break
            tmp_x = dataset[i:x_end_number]
            tmp_y = dataset[x_end_number:y_end_number, 3]
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
        #print(x_train.shape)
        #print(x_test.shape)
        #print(y_train.shape)
        #print(y_test.shape)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1] * x_train.shape[2]))
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1] * x_test.shape[2]))  #x_train과 x_test의 차원 축소
        #print(f"reshape 된 xtrain {x_train.shape}")
        #print(f"reshape 된 xtest {x_test.shape}")

        self.x_trian = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        return self.x_trian, self.y_test, self.y_train, self.y_test

    def create_model(self):
        x_train = self.x_trian
        scaler = StandardScaler()
        scaler.fit(x_train)
        x_train_scaled = scaler.transform(x_train)
        x_test_scaled = scaler.transform(self.x_test)
        model = Sequential()
        model.add(Dense(64, input_shape=(30, 1)))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mse', optimizer='adam', metrics=['mse'])

        early_stopping = EarlyStopping(patience=20)
        x_train_scaled = x_train_scaled.astype(np.float32)
        x_test_scaled = x_test_scaled.astype(np.float32)
        self.y_train = self.y_train.astype(np.float32)
        self.y_test = self.y_test.astype(np.float32)
        np.set_printoptions(threshold=sys.maxsize)

        model.fit(x_train_scaled, self.y_train, validation_split=0.2, verbose=1, batch_size=1, epochs=100, callbacks=[early_stopping])

        loss, mse = model.evaluate(x_test_scaled, self.y_test, batch_size=1)
        print('loss : ', loss)
        print('mse : ', mse)
        y_pred = model.predict(x_test_scaled)

        for i in range(5):
            print('종가 : ', self.y_test[i], '/예측가 : ', y_pred[i])
        file_name = os.path.join(path, "save", "samsung_stock_dnn_model.h5")
        print(f"저장경로: {file_name}")
        model.save(file_name)


