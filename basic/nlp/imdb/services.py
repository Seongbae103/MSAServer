from keras.datasets import imdb
from keras_preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
class ImdbServices(object):
    def __init__(self):
        global train_input, train_target, test_input, test_target, train_input2, val_input, train_target2, val_target
        (train_input, train_target), (test_input, test_target) = imdb.load_data(num_words=500)
        train_input2, val_input, train_target2, val_target = train_test_split(train_input, train_target, test_size=0.2, random_state=42)

    def hook(self):
        self.show_set()
        self.target_checker()
        self.txt_length()

    def show_set(self):
        print(train_target[:20])
        print(train_input.shape, test_input.shape)
        print(len(train_input[0]))
        print(train_input[0])

    def target_checker(self):
        print(train_target2[:20])
        lengths = np.array([len(x) for x in train_input2])
        print(f"평균값, 중간값 {np.mean(lengths)}, {np.median(lengths)}")
        plt.hist(lengths)
        plt.xlabel('lengths')
        plt.ylabel('frequency')
        plt.show()

    def txt_length(self):
        train_seq = pad_sequences(train_input, maxlen=100)
        print(train_seq.shape)
        print(train_seq[0])
        print(train_input[0][:-10])
        print(train_seq[5])
        val_seq = pad_sequences(val_input, maxlen=100)

if __name__ == '__main__':
    ImdbServices().hook()


