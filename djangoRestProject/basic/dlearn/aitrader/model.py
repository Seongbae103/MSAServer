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
    def create(self): pass

    @abstractmethod
    def split_xy5(self, **kwargs): pass

    @abstractmethod
    def basic_scaled(self, param): pass

    @abstractmethod
    def lstm_scaled(self, param): pass

    @abstractmethod
    def fit_model(self, **params): pass

    @abstractmethod
    def fit_ensemble(self, **params): pass


class AiTraderModel(AiTradeBase):
    def __init__(self):
        global path, kospi200, samsung, early_stopping
        path = dir_path('aitrader')
        kospi200 = np.load(os.path.join(path, "data", "kospi200.npy"), allow_pickle=True)
        print('kospi200', kospi200)
        samsung = np.load(os.path.join(path, "data", "samsung   .npy"), allow_pickle=True)
        print('sam ' , samsung)
        early_stopping = EarlyStopping(patience=20)
    def hook(self): # 확인용
        DnnModel().create()
        DnnEnsemble().create()
        LstmModel().create()
        LstmEnsemble().create()
    def create(self):
        pass

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
            tmp_y = dataset[x_end_number:y_end_number, 0]  # 수정
            x.append(tmp_x)
            y.append(tmp_y)
        return np.array(x), np.array(y)

    def basic_scaled(self, param):
        pass

    def lstm_scaled(self, param):
        pass

    def fit_model(selfself, **params):
        pass

    def fit_ensemble(self, **params):
        pass
class DnnModel(AiTraderModel):

    def create(self):
        x_test_scaled, x_train_scaled, y_test, y_train = self.basic_scaled(samsung)
        model = Sequential()
        model.add(Dense(64, input_shape=(25,)))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mse', optimizer='adam', metrics=['mse'])


        x_train_scaled = x_train_scaled.astype(np.float32)
        x_test_scaled = x_test_scaled.astype(np.float32)
        y_train = y_train.astype(np.float32)
        y_test = y_test.astype(np.float32)

        self.fit_model(model, x_test_scaled, x_train_scaled, y_test, y_train)

        file_name = os.path.join(path, "save2", H5FileNames.dnn_model.value)
        model.save(file_name)

    def split_xy5(self):
        pass

    def basic_scaled(self, param):
        x, y = super().split_xy5(dataset=param, time_steps=5, y_column=1)
        print('x',x)
        print('x',x.shape)
        print('y',y)
        print('y',y.shape)
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.3)

        print('스케일 전 y test', y_test)
        x_train = np.reshape(x_train,
                             (x_train.shape[0], x_train.shape[1] * x_train.shape[2]))
        x_test = np.reshape(x_test,
                            (x_test.shape[0], x_test.shape[1] * x_test.shape[2]))
        scaler = StandardScaler()
        scaler.fit(x_train)
        x_train_scaled = scaler.transform(x_train)
        x_test_scaled = scaler.transform(x_test)
        return x_test_scaled, x_train_scaled, y_test, y_train

    def lstm_scaled(self, param):
        pass
    def fit_model(self, model, x_test_scaled, x_train_scaled, y_test, y_train):
        model.fit(x_train_scaled, y_train, validation_split=0.2, verbose=1,
                  batch_size=1, epochs=100, callbacks=[early_stopping])
        loss, mse = model.evaluate(x_test_scaled, y_test, batch_size=1)
        print('loss : ', loss)
        print('mse : ', mse)
        print('y test' ,y_test)
        y_pred = model.predict(x_test_scaled)
        for i in range(5):
            print('종가 : ', y_test[i], '/ 예측가 : ', y_pred[i])

    def fit_ensemble(self, **params): pass

class DnnEnsemble(AiTraderModel):

    def create(self):
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
        self.fit_ensemble(early_stopping, model, x1_test_scaled, x1_train_scaled, x2_test_scaled, x2_train_scaled,
                          y1_test, y1_train)

        file_name = os.path.join(path, "save2", H5FileNames.dnn_ensemble.value)
        model.save(file_name)

    def fit_ensemble(self, early_stopping, model, x1_test_scaled, x1_train_scaled, x2_test_scaled, x2_train_scaled,
                     y1_test, y1_train):
        model.fit([x1_train_scaled, x2_train_scaled], y1_train, validation_split=0.2,
                  verbose=1, batch_size=1, epochs=100,
                  callbacks=[early_stopping])
        loss, mse = model.evaluate([x1_test_scaled, x2_test_scaled], y1_test, batch_size=1)
        print('loss : ', loss)
        print('mse : ', mse)
        y1_pred = model.predict([x1_test_scaled, x2_test_scaled])
        for i in range(5):
            print('종가 : ', y1_test[i], '/ 예측가 : ', y1_pred[i])

    def split_xy5(self):
        pass

    def basic_scaled(self, param):
        pass

    def lstm_scaled(self, param):
        pass

class LstmModel(AiTraderModel):

    def create(self):
        x1_test_scaled, x1_train_scaled, y1_test, y1_train = LstmModel().lstm_scaled(samsung)

        model = Sequential()
        model.add(LSTM(64, input_shape=(5, 5)))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1))

        model.compile(loss='mse', optimizer='adam', metrics=['mse'])

        x_train_scaled = x1_train_scaled.astype(np.float32)
        x_test_scaled = x1_test_scaled.astype(np.float32)
        y_train = y1_train.astype(np.float32)
        y_test = y1_test.astype(np.float32)
        DnnModel().fit_model(model, x_test_scaled, x_train_scaled, y_test, y_train)

        file_name = os.path.join(path, "save2", H5FileNames.lstm_model.value)
        print(f"저장경로: {file_name}")
        model.save(file_name)

    def split_xy5(self):
        pass

    def basic_scaled(self, param):
        pass

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

    def fit_model(selfself, **params):
        pass
    def fit_ensemble(self, **params): pass
class LstmEnsemble(AiTraderModel):

    def create(self):
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

        x1_train_scaled = x1_train_scaled.astype(np.float32)
        x1_test_scaled = x1_test_scaled.astype(np.float32)
        x2_train_scaled = x2_train_scaled.astype(np.float32)
        x2_test_scaled = x2_test_scaled.astype(np.float32)
        y1_train = y1_train.astype(np.float32)
        y1_test = y1_test.astype(np.float32)
        DnnEnsemble().fit_ensemble(early_stopping, model, x1_test_scaled, x1_train_scaled, x2_test_scaled, x2_train_scaled,
                     y1_test, y1_train)
        file_name = os.path.join(path, "save2", H5FileNames.lstm_ensemble.value)
        model.save(file_name)

    def split_xy5(self):
        pass

    def basic_scaled(self, param):
        pass

    def lstm_scaled(self, param):
        pass

    def fit_ensemble(self, **params): pass



if __name__ == '__main__':
    AiTraderModel().hook()