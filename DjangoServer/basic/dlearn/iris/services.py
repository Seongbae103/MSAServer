import os.path

import numpy as np
from keras.saving.save import load_model
from sklearn import datasets

class IrisService(object):

    def __init__(self):
        global model, graph, save, target_names
        save = os.path.join(os.getcwd(),"save")
        model = load_model(os.path.join(save, "iris_model.h5"))
        target_names = datasets.load_iris().target_names

    def find_iris_by_features(self, features): # features = []
        features = np.reshape(features, (1, 4))
        Y_prob = model.predict(features, verbose=0)
        print(f'type is {type(Y_prob)}')
        predicted = Y_prob.argmax(axis=-1)
        return predicted[0]  # p-value 가 가장 높은 것
