import os.path
import numpy as np
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping
from enum import Enum
from keras.models import Model
from keras.layers import Input
from keras.layers import concatenate
from keras.layers import Dense, LSTM
from abc import abstractmethod, ABCMeta
from admin.path import dir_path

class ModelType(Enum):
    dnn_model = 1
    dnn_ensemble = 2
    lstm_model = 3
    lstm_ensemble = 4

class H5FileNames(Enum):
    dnn_model = "samsung_stock_dnn_model.h5"
    dnn_ensemble = "samsung_stock_dnn_ensemble.h5"
    lstm_model = "samsung_stock_lstm_model.h5"
    lstm_ensemble = "samsung_stock_lstm_ensemble.h5"

class AiTradeBase(metaclass = ABCMeta):
    @abstractmethod
    def split_xy5(self, **kwargs): pass

    @abstractmethod
    def hook(self): pass

    @abstractmethod
    def basic_scaled(self, param): pass

    @abstractmethod
    def lstm_scaled(self, param): pass


class AiTraderModel(AiTradeBase):

    def __init__(self):
        global path, kospi200, samsung
        path = dir_path('aitrader')
        kospi200 = np.load(os.path.join(path, "data", "kospi200.npy"), allow_pickle=True)
        samsung = np.load(os.path.join(path, "data", "samsung.npy"), allow_pickle=True)
        print(kospi200)
        print(samsung)
        print(kospi200.shape)
        print(samsung.shape)

    def hook(self):
        DnnModel().hook()
        DnnEnsemble().hook()
        LstmModel().hook()
        LstmEnsemble().hook()

    def split_xy5(self, **kwargs):
        dataset = kwargs["dataset"]
        time_steps = kwargs["time_steps"]
        y_column = kwargs["y_column"]
        x, y = list(), list()
        for i in range(len(dataset)):
            x_end_number = i + time_steps
            y_end_number = x_end_number + y_column  # 수정

            if y_end_number > len(dataset):  # 수정
                break
            tmp_x = dataset[i:x_end_number, :]  # 수정
            tmp_y = dataset[x_end_number:y_end_number, 3]  # 수정
            x.append(tmp_x)
            y.append(tmp_y)
        return np.array(x), np.array(y)

    def basic_scaled(self, param):
        pass

    def lstm_scaled(self, param):
        pass

class DnnModel(AiTraderModel):

    def hook(self):
        x_test_scaled, x_train_scaled, y_test, y_train = self.basic_scaled(samsung)

        model = Sequential()
        model.add(Dense(64, input_shape=(25,)))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mse', optimizer='adam', metrics=['mse'])

        early_stopping = EarlyStopping(patience=20)
        x_train_scaled = x_train_scaled.astype(np.float32)
        x_test_scaled = x_test_scaled.astype(np.float32)
        y_train = y_train.astype(np.float32)
        y_test = y_test.astype(np.float32)

        model.fit(x_train_scaled, y_train, validation_split=0.2, verbose=1,
                  batch_size=1, epochs=100, callbacks=[early_stopping])

        loss, mse = model.evaluate(x_test_scaled, y_test, batch_size=1)
        print('loss : ', loss)
        print('mse : ', mse)
        y_pred = model.predict(x_test_scaled)
        for i in range(5):
            print('종가 : ', y_test[i], '/ 예측가 : ', y_pred[i])
        """
        loss :  691873.625
        mse :  691873.625
        4/4 [==============================] - 0s 669us/step
        종가 :  [52200.] / 예측가 :  [52759.75]
        종가 :  [41450.] / 예측가 :  [41611.36]
        종가 :  [49650.] / 예측가 :  [51578.5]
        종가 :  [44800.] / 예측가 :  [46182.03]
        종가 :  [49500.] / 예측가 :  [49468.492]
        """
        file_name = os.path.join(path, "save2", H5FileNames.dnn_model.value)
        model.save(file_name)

    def basic_scaled(self, param):
        x, y = super().split_xy5(dataset=param, time_steps=5, y_column=1)
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.3)
        x_train = np.reshape(x_train,
                             (x_train.shape[0], x_train.shape[1] * x_train.shape[2]))
        x_test = np.reshape(x_test,
                            (x_test.shape[0], x_test.shape[1] * x_test.shape[2]))
        scaler = StandardScaler()
        scaler.fit(x_train)
        x_train_scaled = scaler.transform(x_train)
        x_test_scaled = scaler.transform(x_test)
        return x_test_scaled, x_train_scaled, y_test, y_train

    def split_xy5(self):
        pass

    def lstm_scaled(self, param):
        pass

class DnnEnsemble(AiTraderModel):
    def hook(self):
        scaled1 = DnnModel().basic_scaled(samsung)
        scaled2 = DnnModel().basic_scaled(kospi200)
        x1_train_scaled, x1_test_scaled, y1_train, y1_test = scaled1
        x2_train_scaled, x2_test_scaled, y2_train, y2_test = scaled2

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

        model = Model(inputs=[input1, input2],
                      outputs=output3)

        model.compile(loss='mse', optimizer='adam', metrics=['mse'])

        early_stopping = EarlyStopping(patience=20)
        x1_train_scaled = x1_train_scaled.astype(np.float32)
        x1_test_scaled = x1_test_scaled.astype(np.float32)
        x2_train_scaled = x2_train_scaled.astype(np.float32)
        x2_test_scaled = x2_test_scaled.astype(np.float32)
        y1_train = y1_train.astype(np.float32)
        y1_test = y1_test.astype(np.float32)
        model.fit([x1_train_scaled, x2_train_scaled], y1_train, validation_split=0.2,
                  verbose=1, batch_size=1, epochs=100,
                  callbacks=[early_stopping])

        loss, mse = model.evaluate([x1_test_scaled, x2_test_scaled], y1_test, batch_size=1)
        print('loss : ', loss)
        print('mse : ', mse)

        y1_pred = model.predict([x1_test_scaled, x2_test_scaled])

        for i in range(5):
            print('종가 : ', y1_test[i], '/ 예측가 : ', y1_pred[i])

        file_name = os.path.join(path, "save2", H5FileNames.dnn_ensemble.value)
        model.save(file_name)

    def split_xy5(self):
        pass

    def basic_scaled(self, param):
        pass

    def lstm_scaled(self, param):
        pass

class LstmModel(AiTraderModel):
    def hook(self):
        x1_test_scaled, x1_train_scaled, y1_test, y1_train = LstmModel().lstm_scaled(samsung)

        model = Sequential()
        model.add(LSTM(64, input_shape=(5, 5)))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1))

        model.compile(loss='mse', optimizer='adam', metrics=['mse'])

        early_stopping = EarlyStopping(patience=20)
        x_train_scaled = x1_train_scaled.astype(np.float32)
        x_test_scaled = x1_test_scaled.astype(np.float32)
        y_train = y1_train.astype(np.float32)
        y_test = y1_test.astype(np.float32)
        model.fit(x_train_scaled, y_train, validation_split=0.2, verbose=1,
                  batch_size=1, epochs=100, callbacks=[early_stopping])

        loss, mse = model.evaluate(x_test_scaled, y_test, batch_size=1)
        print('loss : ', loss)
        print('mse : ', mse)

        y_pred = model.predict(x_test_scaled)

        for i in range(5):
            print('종가 : ', y_test[i], '/ 예측가 : ', y_pred[i])

        file_name = os.path.join(path, "save2", H5FileNames.lstm_model.value)
        print(f"저장경로: {file_name}")
        model.save(file_name)

        '''
        Epoch 44/100

        loss :  1609906.8891261544
        mse :  1609906.625
        종가 :  [52200] / 예측가 :  [51450.69]
        종가 :  [41450] / 예측가 :  [40155.082]
        종가 :  [49650] / 예측가 :  [50907.082]
        종가 :  [44800] / 예측가 :  [45825.527]
        종가 :  [49500] / 예측가 :  [48564.38]
        '''

    def lstm_scaled(self, param):
        x, y = super().split_xy5(dataset=param, time_steps=5, y_column=1)
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.3)
        x_train = np.reshape(x_train,
                             (x_train.shape[0], x_train.shape[1] * x_train.shape[2]))
        x_test = np.reshape(x_test,
                            (x_test.shape[0], x_test.shape[1] * x_test.shape[2]))
        scaler = StandardScaler()
        scaler.fit(x_train)
        x_train_scaled = scaler.transform(x_train)
        x_test_scaled = scaler.transform(x_test)
        x_train_scaled = np.reshape(x_train_scaled,
                                    (x_train_scaled.shape[0], 5, 5))
        x_test_scaled = np.reshape(x_test_scaled,
                                   (x_test_scaled.shape[0], 5, 5))
        return x_test_scaled, x_train_scaled, y_test, y_train

    def split_xy5(self):
        pass

    def basic_scaled(self, param):
        pass


class LstmEnsemble(AiTraderModel):
    def hook(self):
        x1_test_scaled, x1_train_scaled, y1_test, y1_train = LstmModel().lstm_scaled(samsung)
        x2_test_scaled, x2_train_scaled, y2_test, y2_train = LstmModel().lstm_scaled(kospi200)

        input1 = Input(shape=(5, 5))
        dense1 = LSTM(64)(input1)
        dense1 = Dense(32)(dense1)
        dense1 = Dense(32)(dense1)
        output1 = Dense(32)(dense1)

        input2 = Input(shape=(5, 5))
        dense2 = LSTM(64)(input2)
        dense2 = Dense(64)(dense2)
        dense2 = Dense(64)(dense2)
        dense2 = Dense(64)(dense2)
        output2 = Dense(32)(dense2)

        merge = concatenate([output1, output2])
        output3 = Dense(1)(merge)

        model = Model(inputs=[input1, input2],
                      outputs=output3)

        model.compile(loss='mse', optimizer='adam', metrics=['mse'])

        early_stopping = EarlyStopping(patience=20)
        x1_train_scaled = x1_train_scaled.astype(np.float32)
        x1_test_scaled = x1_test_scaled.astype(np.float32)
        x2_train_scaled = x2_train_scaled.astype(np.float32)
        x2_test_scaled = x2_test_scaled.astype(np.float32)
        y1_train = y1_train.astype(np.float32)
        y1_test = y1_test.astype(np.float32)
        model.fit([x1_train_scaled, x2_train_scaled], y1_train, validation_split=0.2,
                  verbose=1, batch_size=1, epochs=100,
                  callbacks=[early_stopping])

        loss, mse = model.evaluate([x1_test_scaled, x2_test_scaled], y1_test, batch_size=1)
        print('loss : ', loss)
        print('mse : ', mse)

        y1_pred = model.predict([x1_test_scaled, x2_test_scaled])

        for i in range(5):
            print('종가 : ', y1_test[i], '/ 예측가 : ', y1_pred[i])

        file_name = os.path.join(path, "save2", H5FileNames.lstm_ensemble.value)
        model.save(file_name)

    def split_xy5(self):
        pass

    def basic_scaled(self, param):
        pass

    def lstm_scaled(self, param):
        pass

if __name__ == '__main__':
    AiTraderModel().hook()