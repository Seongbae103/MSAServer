import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras.callbacks import ModelCheckpoint
import tensorflow_datasets as tfds
'''연습시에는 **kwargs 사용해서'''
class FluitService:
    def __init__(self):
        global trainpath, testpath, Apple_Braeburn_Test, Apple_Braeburn_Train, \
            Apple_Crimson_Snow_Test, Apple_Crimson_Snow_Train, Apple_Golden_1_Test, Apple_Golden_1_Train, \
            Apple_Golden_2_Test, Apple_Golden_2_Train, Apple_Golden_3_Test, Apple_Golden_3_Train, \
            img_height, img_width, batch_size

        fruits = f"C:\\Users\\AIA\\PycharmProjects\\djangoRestProject\\basic\\dlearn\\fruits\\fruits-360-5"
        trainpath = f"{fruits}\\Training"
        testpath = f"{fruits}\\Test"
        Apple_Braeburn_Test = f"{testpath}\\Apple Braeburn"
        Apple_Braeburn_Train = f"{trainpath}\\Apple Braeburn"

        Apple_Crimson_Snow_Test = f"{testpath}\\Apple Crimson Snow"
        Apple_Crimson_Snow_Train = f"{trainpath}\\Apple Crimson Snow"

        Apple_Golden_1_Test = f"{testpath}\\Apple Golden 1"
        Apple_Golden_1_Train = f"{trainpath}\\Apple Golden 1"

        Apple_Golden_2_Test = f"{testpath}\\Apple Golden 2"
        Apple_Golden_2_Train = f"{trainpath}\\Apple Golden 2"
        Apple_Golden_3_Test = f"{testpath}\\Apple Golden 3"
        Apple_Golden_3_Train = f"{trainpath}\\Apple Golden 3"
        img_height = 100
        img_width = 100
        batch_size = 32

        self.class_names = None
        self.train_ds = None
        self.val_ds = None
        self.x = None
        self.y = None

    def show_img(self):
        img = tf.keras.preprocessing.image.load_img \
            (f'{Apple_Golden_3_Train}\\0_100.jpg')
        plt.imshow(img)
        plt.axis("off")
        plt.show()

    def train_dataset(self):
        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            trainpath,
            validation_split=0.3,
            subset="training",
            seed=1,
            image_size=(img_height, img_width),
            batch_size=batch_size)
        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            trainpath,
            validation_split=0.3,
            subset="validation",
            seed=1,
            image_size=(img_height, img_width),
            batch_size=batch_size)
        class_names = train_ds.class_names
        print(f"클래스 이름 {class_names}")
        self.class_names = class_names
        self.train_ds = train_ds
        self.val_ds = val_ds

    def test_dataset(self):
        test_ds = tf.keras.preprocessing.image_dataset_from_directory(
            testpath,
            seed=1,
            image_size=(img_height, img_width),
            batch_size=batch_size)
        type(f"shuffle=True {test_ds}")
        y = np.concatenate([y for x, y in test_ds], axis=0)
        print(f"shuffle=True의 y에 저장  {y}")
        self.y = y
        self.test_ds = test_ds

    def test_dataset_shuffle(self):
        test_ds1 = tf.keras.preprocessing.image_dataset_from_directory(
            testpath,
            seed=1,
            image_size=(img_height, img_width),
            batch_size=batch_size,
            shuffle=False)
        type(f"shuffle=False {test_ds1}")
        y1 = np.concatenate([y for x, y in test_ds1], axis=0)
        print(f"shuffle=Fales의 y에 저장 {y1}")
        x = np.concatenate([x for x, y in test_ds1], axis=0)
        print(x[0])
        self.x = x
        self.test_ds1 = test_ds1

    def show_train_first(self):
        plt.figure(figsize=(3, 3))
        plt.imshow(self.x[0].astype("uint8"))
        plt.title(self.class_names[self.y[0]])
        plt.axis("off")
        plt.show()

    def show_train_last(self):
        plt.figure(figsize=(3, 3))
        plt.imshow(self.x[-1].astype("uint8"))
        plt.title(self.class_names[self.y[-1]])
        plt.axis("off")
        plt.show()

    def modify_prefetch(self):
        BUFFER_SIZE = 10000
        AUTOTUNE = tf.data.experimental.AUTOTUNE
        train_ds = self.train_ds.cache().shuffle(BUFFER_SIZE).prefetch(buffer_size=AUTOTUNE)
        val_ds = self.val_ds.cache().prefetch(buffer_size=AUTOTUNE)
        test_ds = self.test_ds.cache().prefetch(buffer_size=AUTOTUNE)
        print(f"trainds 타입 : {type(self.train_ds)}")

    def create_model(self):
        num_classes = 5
        model = tf.keras.Sequential([
            keras.layers.experimental.preprocessing.Rescaling(1. / 255, input_shape=(img_height, img_width, 3)),
            keras.layers.Conv2D(16, 3, padding='same', activation='relu'),
            keras.layers.MaxPooling2D(2),
            keras.layers.Dropout(.50),
            keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
            keras.layers.MaxPooling2D(2),
            keras.layers.Dropout(.50),
            keras.layers.Flatten(),
            keras.layers.Dense(500, activation='relu'),
            keras.layers.Dropout(.50),
            keras.layers.Dense(num_classes, activation='softmax')
        ])
        model.summary()

        model.compile(
            optimizer='adam',
            loss=tf.losses.SparseCategoricalCrossentropy(),
            metrics=['accuracy'])
        checkpointer = ModelCheckpoint('CNNClassifier.h5', save_best_only=True)
        early_stopping_cb = keras.callbacks.EarlyStopping(patience=5, monitor='val_accuracy',
                                                          restore_best_weights=True)
        epochs = 20
        history = model.fit(
            self.train_ds,
            batch_size=batch_size,
            validation_data=self.val_ds,
            epochs=epochs,
            callbacks=[checkpointer, early_stopping_cb]
        )
        len(history.history['val_accuracy'])

        acc = history.history['accuracy']
        val_acc = history.history['val_accuracy']

        loss = history.history['loss']
        val_loss = history.history['val_loss']

        epochs_range = range(1, len(acc) + 1)

        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, acc, label='Training Accuracy')
        plt.plot(epochs_range, val_acc, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.title('Training and Validation Accuracy')

        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, loss, label='Training Loss')
        plt.plot(epochs_range, val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.title('Training and Validation Loss')
        plt.show()

        '''--- 이 위로 model/ 아래로 service ---'''

        model.load_weights('CNNClassifier.h5')
        test_loss, test_acc = model.evaluate(self.test_ds)

        print("test loss: ", test_loss)
        print()
        print("test accuracy: ", test_acc)
        predictions = model.predict(self.test_ds1)
        score = tf.nn.softmax(predictions[0])

        print(
            "This image most likely belongs to {} with a {:.2f} percent confidence."
            .format(self.class_names[np.argmax(score)], 100 * np.max(score))
        )
        score = tf.nn.softmax(predictions[-1])

        print(
            "This image most likely belongs to {} with a {:.2f} percent confidence."
            .format(self.class_names[np.argmax(score)], 100 * np.max(score))
        )
    def hook(self):
        self.train_dataset()
        self.test_dataset()
        self.test_dataset_shuffle()
        self.show_train_first()
        self.show_train_last()
        self.modify_prefetch()
        self.create_model()

if __name__ == '__main__':
    FluitService().hook()