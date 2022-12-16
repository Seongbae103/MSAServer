import os.path

import matplotlib.pyplot as plt
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
class FashionService(object):
    def __init__(self):
        global class_names
        class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                     'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']


    def service_model(self, i) -> '':
        model = load_model(r"C:/Users/AIA/PycharmProjects/djangoRestProject/shop/save/fashion_model.h5")
        (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.fashion_mnist.load_data()
        predictions = model.predict(test_images)
        predictions_array, true_label, img = predictions[i], test_labels[i], test_images[i]
        result = np.argmax(predictions_array)
        print(f"예측한 답 : {result}")
        '''if predicted_label == true_label:
            color = "blue"
        else:
            color = 'red'
            plt.xlabel('{} {:2.0f}% ({})'.format(
                class_names[true_label],
                100 * np.max(predictions_array),
                class_names[true_label]
            ), color=color)
        plt.show()'''
        if result == 0:
            resp = 'T-shirt/top'
        elif result == 1:
            resp = 'Trouser'
        elif result == 2:
            resp = 'Pullover'
        elif result == 3:
            resp = 'Dress'
        elif result == 4:
            resp = 'Coat'
        elif result == 5:
            resp = 'Sandal'
        elif result == 6:
            resp = 'Shirt'
        elif result == 7:
            resp = 'Sneaker'
        elif result == 8:
            resp = 'Bag'
        elif result == 9:
            resp = 'Ankle boot'
        return resp



MENUS = ["종료", #0
            "데이터구조파악",
            "전체 실행"]

fsmenu = {
    "1" : lambda t : t.service_model()
}

if __name__ == '__main__':

    t = FashionService()
    while True:
        [print(f"{i}. {j}") for i, j in enumerate(fsmenu)]
        menu = input('메뉴선택: ')
        if menu == 0:
            print("종료")
            break
        else:
            try:
                fsmenu[menu](t)
            except KeyError as e:
                if 'some error message' in str(e):
                    print('Caught error message')
                else:
                    print("Didn't catch error message")
