from matplotlib import pyplot as plt
from tensorflow import keras


class ImdbModel(object):
    def __init__(self):
        pass

    def create(self, train_seq, val_seq):
        global model, train_oh, val_oh
        model = keras.Sequential()
        sample_length = 100
        freq_words = 500 #빈도수가 가장 높은 단어 500개
        model.add(keras.layers.SimpleRNN(sample_length, input_shape=(sample_length, freq_words)))
        model.add(keras.layers.Dense(1, activation='sigmoid'))
        train_oh = keras.utils.to_categorical(train_seq) #oh is OneHotEncoding
        print(train_oh.shape)
        print(train_oh[0][0][:12])
        val_oh = keras.utils.to_categorical(val_seq)

    def fit(self,train_target, val_target):
        rmsprop = keras.optimizers.RMSprop(learning_rate=1e-4)
        model.compile(optimizer=rmsprop, loss='binary_crossentropy',
                           metrics = ['accuracy'])
        checkpoint_cb = keras.callbacks.ModelCheckpoint('best-simple-model.h5', save_best_only=True)
        early_stopping_cb = keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)
        history = model.fit(train_oh, train_target, epochs=100, batch_size = 64,
                            validation_data =(val_oh, val_target),
                            callbacks=[checkpoint_cb, early_stopping_cb])
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.xlabel('epoch')
        plt.ylabel('loss')
        plt.legend(['train', 'val'])
        plt.show()

