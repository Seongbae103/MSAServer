import os.path
import numpy as np
from sklearn.preprocessing import StandardScaler
from api.path import dir_path
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping
from enum import Enum
from keras.models import Model
from keras.layers import Dense, Input
from keras.layers import concatenate
from keras.layers import Dense, LSTM
from abc import abstractmethod, ABCMeta

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

class AiTradeBase(metaclass=ABCMeta):

    @abstractmethod
    def create(self): pass

    @abstractmethod
    def split(self, **kwargs): pass

    @abstractmethod
    def preprocess(self): pass

    @abstractmethod
    def compile(self): pass

    @abstractmethod
    def postprocess(self, **kwargs): pass

class AiTraderModel(AiTradeBase):

    def __init__(self):
        global path, kospi200, samsung
        path = dir_path('aitrader')
        kospi200 = np.load(os.path.join(path, "save", "kospi200.npy"), allow_pickle=True)
        samsung = np.load(os.path.join(path, "save", "samsung.npy"), allow_pickle=True)
        print(kospi200)
        print(samsung)
        print(kospi200.shape)
        print(samsung.shape)

    def create(self):
        super(AiTraderModel, self).create()

    def split(self, **kwargs):
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

    def preprocess(self):
        super(AiTraderModel, self).preprocess()

    def compile(self):
        super(AiTraderModel, self).compile()

    def postprocess(self, **kwargs):
        super(AiTraderModel, self).postprocess(kwargs)


class DnnModel(AiTraderModel):

    def create(self):
        x_train_scaled,x_test_scaled,y_train,y_test = self.preprocess()
        model = self.compile()
        self.postprocess(model=model,
                         x_train_scaled=x_train_scaled,
                         x_test_scaled=x_test_scaled,
                         y_train=y_train,
                         y_test=y_test)

    def preprocess(self):
        x, y = self.split(dataset=samsung, time_steps=5, y_column=1)
        x_train, x_test, y_train, y_test =\
            train_test_split(x, y, random_state=1, test_size=0.3)
        x_train = np.reshape(x_train,
                             (x_train.shape[0], x_train.shape[1] * x_train.shape[2]))
        x_test = np.reshape(x_test,
                            (x_test.shape[0], x_test.shape[1] * x_test.shape[2]))
        scaler = StandardScaler()
        scaler.fit(x_train)
        x_train_scaled = scaler.transform(x_train)
        x_test_scaled = scaler.transform(x_test)
        return x_train_scaled,x_test_scaled,y_train,y_test

    def compile(self):
        model = Sequential()
        model.add(Dense(64, input_shape=(25,)))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mse', optimizer='adam', metrics=['mse'])
        return model

    def postprocess(self, **kwargs):
        model = kwargs["model"]
        x_train_scaled = kwargs["x_train_scaled"].astype(np.float32)
        x_test_scaled = kwargs["x_test_scaled"].astype(np.float32)
        y_train = kwargs["y_train"].astype(np.float32)
        y_test = kwargs["y_test"].astype(np.float32)
        early_stopping = EarlyStopping(patience=20)
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
        file_name = os.path.join(path, "save", H5FileNames.dnn_model.value)
        model.save(file_name)


class DnnEnsemble(AiTraderModel):

    def create(self):
        x1_train_scaled, x1_test_scaled, \
        x2_train_scaled, x2_test_scaled, \
        y1_train, y1_test, \
        y2_train, y2_test = \
            self.preprocess()
        model = self.compile()
        self.postprocess(model=model,
                         x1_test_scaled=x1_test_scaled,
                         x1_train_scaled=x1_train_scaled,
                         x2_test_scaled=x2_test_scaled,
                         x2_train_scaled=x2_train_scaled,
                         y1_test=y1_test,
                         y1_train=y1_train)

    def preprocess(self):
        x1, y1 = self.split(dataset=samsung,
                            time_steps=5,
                            y_column=1)
        x2, y2 = self.split(dataset=kospi200,
                            time_steps=5,
                            y_column=1)
        x1_train, x1_test, y1_train, y1_test = train_test_split(
            x1, y1, random_state=1, test_size=0.3)
        x2_train, x2_test, y2_train, y2_test = train_test_split(
            x2, y2, random_state=2, test_size=0.3)
        x1_train = np.reshape(x1_train,
                              (x1_train.shape[0], x1_train.shape[1] * x1_train.shape[2]))
        x1_test = np.reshape(x1_test,
                             (x1_test.shape[0], x1_test.shape[1] * x1_test.shape[2]))
        x2_train = np.reshape(x2_train,
                              (x2_train.shape[0], x2_train.shape[1] * x2_train.shape[2]))
        x2_test = np.reshape(x2_test,
                             (x2_test.shape[0], x2_test.shape[1] * x2_test.shape[2]))
        scaler1 = StandardScaler()
        scaler1.fit(x1_train)
        x1_train_scaled = scaler1.transform(x1_train)
        x1_test_scaled = scaler1.transform(x1_test)
        scaler2 = StandardScaler()
        scaler2.fit(x2_train)
        x2_train_scaled = scaler2.transform(x2_train)
        x2_test_scaled = scaler2.transform(x2_test)
        return x1_train_scaled, x1_test_scaled, \
               x2_train_scaled, x2_test_scaled, \
               y1_train, y1_test, \
               y2_train, y2_test,

    def compile(self):
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
        return model

    def postprocess(self, **kwargs):
        model = kwargs["model"]
        x1_train_scaled = kwargs["x1_train_scaled"].astype(np.float32)
        x1_test_scaled = kwargs["x1_test_scaled"].astype(np.float32)
        x2_train_scaled = kwargs["x2_train_scaled"].astype(np.float32)
        x2_test_scaled = kwargs["x2_test_scaled"].astype(np.float32)
        y1_train = kwargs["y1_train"].astype(np.float32)
        y1_test = kwargs["y1_test"].astype(np.float32)
        early_stopping = EarlyStopping(patience=20)
        model.fit([x1_train_scaled, x2_train_scaled], y1_train, validation_split=0.2,
                  verbose=1, batch_size=1, epochs=100,
                  callbacks=[early_stopping])
        loss, mse = model.evaluate([x1_test_scaled, x2_test_scaled], y1_test, batch_size=1)
        print('loss : ', loss)
        print('mse : ', mse)
        y1_pred = model.predict([x1_test_scaled, x2_test_scaled])
        for i in range(5):
            print('종가 : ', y1_test[i], '/ 예측가 : ', y1_pred[i])
        file_name = os.path.join(path, "save", H5FileNames.dnn_ensemble.value)
        model.save(file_name)
        '''
            loss :  1348967.9961648777
            mse :  1348968.125
            종가 :  [52200] / 예측가 :  [50549.504]
            종가 :  [41450] / 예측가 :  [41341.992]
            종가 :  [49650] / 예측가 :  [49872.363]
            종가 :  [44800] / 예측가 :  [45122.33]
            종가 :  [49500] / 예측가 :  [48873.23]
            '''
class LstmModel(AiTraderModel):

    def create(self):
        x_test_scaled, x_train_scaled, y_test, y_train = self.preprocess()
        model = self.compile()
        self.postprocess(model=model,
                         x_test_scaled=x_test_scaled,
                         x_train_scaled=x_train_scaled,
                         y_test=y_test,
                         y_train=y_train)

    def postprocess(self, **kwargs):
        early_stopping = EarlyStopping(patience=20)
        x_train_scaled = kwargs["x_train_scaled"].astype(np.float32)
        x_test_scaled = kwargs["x_test_scaled"].astype(np.float32)
        y_train = kwargs["y_train"].astype(np.float32)
        y_test = kwargs["y_test"].astype(np.float32)
        model = kwargs["model"]
        model.fit(x_train_scaled, y_train, validation_split=0.2, verbose=1,
                  batch_size=1, epochs=100, callbacks=[early_stopping])
        loss, mse = model.evaluate(x_test_scaled, y_test, batch_size=1)
        print('loss : ', loss)
        print('mse : ', mse)
        y_pred = model.predict(x_test_scaled)
        for i in range(5):
            print('종가 : ', y_test[i], '/ 예측가 : ', y_pred[i])
        file_name = os.path.join(path, "save", H5FileNames.lstm_model.value)
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

    def compile(self):
        model = Sequential()
        model.add(LSTM(64, input_shape=(5, 5)))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mse', optimizer='adam', metrics=['mse'])
        return model

    def preprocess(self):
        x, y = self.split(dataset=samsung, time_steps=5, y_column=1)
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

class LstmEnsemble(AiTraderModel):

    def create(self):
        x1_test_scaled, x1_train_scaled, x2_test_scaled, x2_train_scaled, y1_test, y1_train = self.preprocess()
        model = self.compile()
        self.postprocess(model=model,
                         x1_test_scaled=x1_test_scaled,
                         x1_train_scaled=x1_train_scaled,
                         x2_test_scaled=x2_test_scaled,
                         x2_train_scaled=x2_train_scaled,
                         y1_test=y1_test,
                         y1_train=y1_train)

    def postprocess(self, **kwargs):
        early_stopping = EarlyStopping(patience=20)
        x1_train_scaled = kwargs["x1_train_scaled"].astype(np.float32)
        x1_test_scaled = kwargs["x1_test_scaled"].astype(np.float32)
        x2_train_scaled = kwargs["x2_train_scaled"].astype(np.float32)
        x2_test_scaled = kwargs["x2_test_scaled"].astype(np.float32)
        y1_train = kwargs["y1_train"].astype(np.float32)
        y1_test = kwargs["y1_test"].astype(np.float32)
        model = kwargs["model"]
        model.fit([x1_train_scaled, x2_train_scaled], y1_train, validation_split=0.2,
                  verbose=1, batch_size=1, epochs=100,
                  callbacks=[early_stopping])
        loss, mse = model.evaluate([x1_test_scaled, x2_test_scaled], y1_test, batch_size=1)
        print('loss : ', loss)
        print('mse : ', mse)
        y1_pred = model.predict([x1_test_scaled, x2_test_scaled])
        for i in range(5):
            print('종가 : ', y1_test[i], '/ 예측가 : ', y1_pred[i])
        file_name = os.path.join(path, "save", H5FileNames.lstm_ensemble.value)
        model.save(file_name)
        '''
            loss :  1125525.833051306
            mse :  1125525.625
            종가 :  [52200] / 예측가 :  [53270.87]
            종가 :  [41450] / 예측가 :  [40059.094]
            종가 :  [49650] / 예측가 :  [50577.68]
            종가 :  [44800] / 예측가 :  [46032.695]
            종가 :  [49500] / 예측가 :  [50204.047]
            '''

    def compile(self):
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
        return model

    def preprocess(self):
        x1, y1 = self.split(dataset=samsung,
                            time_steps=5,
                            y_column=1)
        x2, y2 = self.split(dataset=kospi200,
                            time_steps=5,
                            y_column=1)
        x1_train, x1_test, y1_train, y1_test = train_test_split(
            x1, y1, random_state=1, test_size=0.3)
        x2_train, x2_test, y2_train, y2_test = train_test_split(
            x2, y2, random_state=2, test_size=0.3)
        x1_train = np.reshape(x1_train,
                              (x1_train.shape[0], x1_train.shape[1] * x1_train.shape[2]))
        x1_test = np.reshape(x1_test,
                             (x1_test.shape[0], x1_test.shape[1] * x1_test.shape[2]))
        x2_train = np.reshape(x2_train,
                              (x2_train.shape[0], x2_train.shape[1] * x2_train.shape[2]))
        x2_test = np.reshape(x2_test,
                             (x2_test.shape[0], x2_test.shape[1] * x2_test.shape[2]))
        scaler1 = StandardScaler()
        scaler1.fit(x1_train)
        x1_train_scaled = scaler1.transform(x1_train)
        x1_test_scaled = scaler1.transform(x1_test)
        scaler2 = StandardScaler()
        scaler2.fit(x2_train)
        x2_train_scaled = scaler2.transform(x2_train)
        x2_test_scaled = scaler2.transform(x2_test)
        print(x2_train_scaled[0, :])
        x1_train_scaled = np.reshape(x1_train_scaled,
                                     (x1_train_scaled.shape[0], 5, 5))
        x1_test_scaled = np.reshape(x1_test_scaled,
                                    (x1_test_scaled.shape[0], 5, 5))
        x2_train_scaled = np.reshape(x2_train_scaled,
                                     (x2_train_scaled.shape[0], 5, 5))
        x2_test_scaled = np.reshape(x2_test_scaled,
                                    (x2_test_scaled.shape[0], 5, 5))
        return x1_test_scaled, x1_train_scaled, x2_test_scaled, x2_train_scaled, y1_test, y1_train
