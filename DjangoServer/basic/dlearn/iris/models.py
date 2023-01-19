import os.path

import pandas as pd
import tensorflow as tf
from keras import Sequential
from keras.layers import Dense
from sklearn import datasets
from sklearn.preprocessing import OneHotEncoder

'''
Iris Species
Classify iris plants into three species in this classic dataset
'''
class IrisModel(object):

    def __init__(self):
        global iris, X, Y, save
        iris = datasets.load_iris()
        print(f'type {type(iris)}') # type <class 'sklearn.utils._bunch.Bunch'>
        X = iris.data
        Y = iris.target
        save = os.path.join(os.getcwd(),"save")

    def spec(self):
        print(" --- 1.Features ---")
        print(iris['feature_names'])
        print(" --- 2.target ---")
        print(iris['target'])
        print(" --- 3.print ---")
        print(iris)
        '''
        Shape (150, 6)
        ['Id', 'SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm','Species']
        
        print(" --- 1.Shape ---")
        print(iris.shape)
        print(" --- 2.Features ---")
        print(iris.columns)
        print(" --- 3.Info ---")
        print(iris.info())
        print(" --- 4.Case Top1 ---")
        print(iris.head(1))
        print(" --- 5.Case Bottom1 ---")
        print(iris.tail(3))
        print(" --- 6.Describe ---")
        print(iris.describe())
        print(" --- 7.Describe All ---")
        print(iris.describe(include='all'))
        '''

    def create_model(self):
        enc = OneHotEncoder()
        Y_1hot = enc.fit_transform(Y.reshape(-1,1)).toarray()
        model = Sequential()
        model.add(Dense(4, input_dim=4, activation='relu'))
        model.add(Dense(3, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(X, Y_1hot, epochs=300, batch_size=10)
        model.save(os.path.join(save, "iris_model.h5"))





