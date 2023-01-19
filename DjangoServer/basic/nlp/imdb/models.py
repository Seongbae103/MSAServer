import os

from matplotlib import pyplot as plt
from tensorflow import keras

class ImdbModel(object):

    def __init__(self):
        global model_name, rmsprop, binary_crossentropy, accuracy, sigmoid
        model_name = os.path.join(os.getcwd(), 'data/best-simplernn-model.h5')
        rmsprop = keras.optimizers.RMSprop(learning_rate=1e-4)
        binary_crossentropy = 'binary_crossentropy'
        accuracy = ['accuracy']
        sigmoid = 'sigmoid'

    def create(self, train_seq, val_seq):
        global model, train_oh, val_oh
        model = keras.Sequential()
        sample_length = 100
        freq_words = 500
        model.add(keras.layers.SimpleRNN(8, input_shape=(sample_length, freq_words)))
        model.add(keras.layers.Dense(1, activation=sigmoid))
        train_oh = keras.utils.to_categorical(train_seq) # oh is OneHotEncoding
        print(train_oh.shape)
        print(train_oh[0][0][:12])
        val_oh = keras.utils.to_categorical(val_seq)

    def fit(self, train_target, val_target):
        model.compile(optimizer=rmsprop, loss=binary_crossentropy,
                           metrics=accuracy)
        checkpoint_cb = keras.callbacks.ModelCheckpoint(model_name,
                                                        save_best_only=True)
        early_stopping_cb = keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)
        history = model.fit(train_oh, train_target, epochs=100, batch_size=64,
                            validation_data=(val_oh, val_target),
                            callbacks=[checkpoint_cb, early_stopping_cb])
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.xlabel('epoch')
        plt.ylabel('loss')
        plt.legend(['train', 'val'])
        plt.show()

class NaverMovieModel(object):
    def __init__(self):
        pass

