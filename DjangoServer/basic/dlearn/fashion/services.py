import numpy as np
from keras.saving.save import load_model
import os
from tensorflow import keras


class FashionService(object):
    def __init__(self):
        global class_names, fashion_model, save
        save = os.path.join(os.getcwd(),"save")
        class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                       'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
        fashion_model = os.path.join(save, "fashion_model.h5")

    # self, i, predictions_array, true_label, img
    def find_fashion_by_index(self, i) -> '':
        model = load_model(fashion_model)
        (train_images, train_labels), (test_images, test_labels) = keras.datasets.fashion_mnist.load_data()
        predictions = model.predict(test_images)
        predictions_array, true_label, img = predictions[i], test_labels[i], test_images[i]
        '''
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(img, cmap=plt.cm.binary)
        '''
        result = np.argmax(predictions_array)
        print(f"예측한 답 : {result}")
        '''
        if predicted_label == true_label:
            color = 'blue'
        else:
            color = 'red'
        
        plt.xlabel('{} {:2.0f}% ({})'.format(
            class_names[predicted_label],
            100 * np.max(predictions_array),
            class_names[true_label]
        ), color = color)
        plt.show()
        '''
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
        print(f"패션 서비스에서 예측한 값: {resp}")
        return resp

