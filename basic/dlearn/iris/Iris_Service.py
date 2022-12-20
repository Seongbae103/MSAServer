import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn import datasets
from keras.saving.save import load_model
from tensorflow.python.framework.ops import get_default_graph



'''
Iris Species
Classify iris plants into three species in this classic dataset
'''
class IrisService(object):
    def __init__(self):
        global model, graph, target_names
        model = load_model('save/iris_model.h5')
        target_names = datasets.load_iris().target_names

    def hook(self):
        self.service_model()

    def service_model(self, features):
        features = np.reshape(features, (1, 4))
        Y_prob = model.predict(features, verbose=0)
        print(f'type is {type(Y_prob)}')
        predicted = Y_prob.argmax(axis=-1)
        return predicted[0]


IRIS_MENUS = ["종료", #0
            "데이터구조파악",
            "전체 실행"]

iris_menu = {
    "1" : lambda t : t.hook(),
}

if __name__ == '__main__':

    t = IrisService()
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
