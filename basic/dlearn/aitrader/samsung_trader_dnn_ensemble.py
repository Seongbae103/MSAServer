import os

import numpy as np
from keras import Input
from keras.callbacks import EarlyStopping
from keras.layers import Dense, concatenate

from keras.models import Model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from admin.path import dir_path

kospi200 = np.load('./data/kospi200.npy', allow_pickle=True)
samsung = np.load('./data/samsung.npy', allow_pickle=True)
class SamsungTraderDnnEnsemble(object):
    def __init__(self):
        global path
        path = dir_path('aitrader')


    def split_xy5(self, dataset, time_steps, y_column):
        x, y = list(), list()
        for i in range(len(dataset)):
            x_end_number = i + time_steps
            y_end_number = x_end_number + y_column
            if y_end_number > len(dataset):
                break
            tmp_x = dataset[i:x_end_number, :]
            tmp_y = dataset[i:y_end_number, 3]
            x.append(tmp_x)
            y.append(tmp_y)
        return np.array(x), np.array(y)


    def create_dnn_ensemble(self):
        x1, y1 = self.split_xy5(samsung, 5, 1)
        x2, y2 = self.split_xy5(kospi200, 5, 1)
        x1_train, x1_test, y1_train, y1_test = train_test_split(x1, y1, random_state=1, test_size =0.3)
        x2_train, x2_test, y2_train, y2_test = train_test_split(x2, y2, random_state=1, test_size =0.3)

        print(x1_train.shape)
        print(x1_test.shape)
        print(x2_train.shape)
        print(x2_test.shape)

        x1_train = np.reshape(x1_train, (x1_train.shape[0], x1_train.shape[1] * x1_train.shape[2]))
        x1_test = np.reshape(x1_test, (x1_test.shape[0], x1_test.shape[1] * x1_test.shape[2]))
        x2_train = np.reshape(x2_train, (x2_train.shape[0], x2_train.shape[1] * x2_train.shape[2]))
        x2_test = np.reshape(x2_test, (x2_test.shape[0], x2_test.shape[1] * x2_test.shape[2]))
        print(x1_train.shape)
        print(x1_test.shape)
        print(x2_train.shape)
        print(x2_test.shape)

        scalard1 = StandardScaler()
        scalard1.fit(x1_train)
        x1_train_scaled = scalard1.transform(x1_train)
        x1_test_scaled = scalard1.transform(x1_test)
        scalard2 = StandardScaler()
        scalard2.fit(x2_train)
        x2_train_scaled = scalard2.transform(x2_train)
        x2_test_scaled = scalard2.transform(x2_test)
        print(f"input {x1_train_scaled.shape}")
        print(f"input {x2_train_scaled.shape}")
        input1 = Input(shape=(25,))
        dense1 = Dense(64)(input1)
        dense1 = Dense(32)(dense1)
        dense1 = Dense(32)(dense1)
        output1 = Dense(32)(dense1)

        input2 = Input(shape=(25,))
        dense2 = Dense(64)(input2)
        dense2 = Dense(64)(dense2)
        dense2 = Dense(64)(dense2)
        dense2 = Dense(64)(dense2)
        output2 = Dense(32)(dense2)

        merge = concatenate([output1, output2])
        output3 = Dense(1)(merge)
        model = Model(inputs=[input1, input2], outputs= output3)
        model.compile(loss='mse', optimizer='adam', metrics=['mse'])
        early_stopping = EarlyStopping(patience=20)
        x1_train_scaled= x1_train_scaled.astype(np.float32)
        x1_test_scaled = x1_test_scaled.astype(np.float32)
        x2_train_scaled = x2_train_scaled.astype(np.float32)
        x2_test_scaled = x2_test_scaled.astype(np.float32)
        y1_train = y1_train.astype(np.float32)
        y1_test = y1_test.astype(np.float32)

        model.fit([x1_train_scaled, x2_train_scaled], y1_train, validation_split=0.2, verbose=1, batch_size=1, epochs=100,
                  callbacks=[early_stopping])  # fit : batch_size, epochs

        loss, mse = model.evaluate([x1_test_scaled, x2_test_scaled], y1_test, batch_size=1)  # test(반복x)
        print('loss : ', loss)
        print('mse : ', mse)
        y1_pred = model.predict([x1_test_scaled, x2_test_scaled])

        for i in range(5):
            print('종가 : ', y1_test[i], '/예측가 : ', y1_pred[i])
        file_name = os.path.join(path, "save", "samsung_stock_dnn_ensemble.h5")
        print(f"저장경로: {file_name}")
        model.save(file_name)


if __name__ == '__main__':
    SamsungTraderDnnEnsemble().create_dnn_ensemble()