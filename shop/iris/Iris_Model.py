import pandas as pd
import tensorflow as tf
from keras.layers import Dense
from keras import Sequential
from sklearn import datasets
from sklearn.preprocessing import OneHotEncoder



'''
Iris Species
Classify iris plants into three species in this classic dataset
'''
class Iris(object):
    def __init__(self):
        self.iris = datasets.load_iris()
        print(f'type {type(self.iris)}') # 타입체크 type <class 'sklearn.utils.Bunch'>
        self._X = self.iris.data
        self._Y = self.iris.target


    def spec(self):
        iris = self.iris
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
        shape : (150, 6)
        ['Id', 'SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species']
        '''
    def create_model(self): #분류 (회기시는 모양이 다르다)
        X = self._X
        Y = self._Y
        enc = OneHotEncoder()
        Y_1hot = enc.fit_transform(Y.reshape(-1,1)).toarray()
        model = Sequential()
        model.add(Dense(4, input_dim=4, activation='relu')) # relu
        model.add(Dense(3, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(X, Y_1hot, epochs=300, batch_size=10)
        print('Model Training is comleted')
        file_name = 'save/iris_model.h5'
        model.save(file_name)
        print(f'Model Saved in {file_name}')

    def hook(self):
        self.create_model()

IRIS_MENUS = ["종료", #0
            "데이터구조파악",
            "전체 실행"]

iris_menu = {
    "1" : lambda t : t.hook(),
    "2" : lambda t : t.spec(),
}

if __name__ == '__main__':

    t = Iris()
    while True:
        [print(f"{i}. {j}") for i, j in enumerate(iris_menu)]
        menu = input('메뉴선택: ')
        if menu == 0:
            print("종료")
            break
        else:
            try:
                iris_menu[menu](t)
            except KeyError as e:
                if 'some error message' in str(e):
                    print('Caught error message')
                else:
                    print("Didn't catch error message")
