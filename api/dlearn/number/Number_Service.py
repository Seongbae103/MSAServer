import numpy as np
import tensorflow as tf
from keras.saving.save import load_model
from matplotlib import pyplot as plt


class NumberService(object):
    def __init__(self):
        global class_names
        class_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


    def service_model(self, i) -> '':
        model = load_model(r"/api/dlearn/save/number_model.h5")
        (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.fashion_mnist.load_data()
        predictions = model.predict(test_images)
        predictions_array, true_label, img = predictions[i], test_labels[i], test_images[i]
        plt.show()
        result = np.argmax(predictions_array)
        print(f"예측한 답 : {result}")
        if result == 0:
            resp = '0'
        elif result == 1:
            resp = '1'
        elif result == 2:
            resp = '2'
        elif result == 3:
            resp = '3'
        elif result == 4:
            resp = '4'
        elif result == 5:
            resp = '5'
        elif result == 6:
            resp = '6'
        elif result == 7:
            resp = '7'
        elif result == 8:
            resp = '8'
        elif result == 9:
            resp = '9'
        return resp



MENUS = ["종료", #0
]

fsmenu = {
    "1" : lambda t : t.service_model()
}

if __name__ == '__main__':

    t = NumberService()
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
