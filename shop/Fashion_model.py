import os

import keras.layers
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from keras.layers import Dense
from keras import Sequential
from keras.models import load_model
from sklearn import datasets
from sklearn.preprocessing import OneHotEncoder



'''
Iris Species
Classify iris plants into three species in this classic dataset
'''
class FashionModel(object):

    def hook(self):
        self.create_model()

    def create_model(self): #분류 (회기시는 모양이 다르다)
        (train_imges, train_labels), (test_imges, test_labels) = tf.keras.datasets.fashion_mnist.load_data()
        plt.figure()
        plt.imshow(train_imges[10])
        plt.colorbar()
        plt.grid(False)
        plt.show()
        model = Sequential([
            keras.layers.Flatten(input_shape=(28,28)),  #입력층
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dense(10, activation='softmax') #출력층 "class_names"의 요소 중 하나니까 10
        ])
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        model.fit(train_imges, train_labels, epochs=5)
        test_loss, test_acc = model.evaluate(test_imges, test_labels)
        print(f'Test Accuracy is {test_acc}')
        file_name = load_model(r"C:\Users\AIA\PycharmProjects\djangoRestProject\shop\save\fashion_model.h5")
        print(f'저장경로: {file_name}')
        model.save(file_name)

MODEL_MENUS = ["종료", #0
            "데이터구조파악",
            "전체 실행"]

model_menu = {
    "1" : lambda t : t.hook()
}

if __name__ == '__main__':

    t = FashionModel()
    while True:
        [print(f"{i}. {j}") for i, j in enumerate(model_menu)]
        menu = input('메뉴선택: ')
        if menu == 0:
            print("종료")
            break
        else:
            try:
                model_menu[menu](t)
            except KeyError as e:
                if 'some error message' in str(e):
                    print('Caught error message')
                else:
                    print("Didn't catch error message")
