import os
from api.path import fruits
import numpy as np
import matplotlib.pyplot as plt
from keras.callbacks import ModelCheckpoint
import tensorflow as tf
from keras.saving.save import load_model
from keras import layers
from tensorflow import keras

class FruitsModel:
    def __init__(self):
        global class_names, Apple_Braeburn_Test, Apple_Braeburn_Train, \
            Apple_Crimson_Snow_Train, Apple_Golden_1_Train, Apple_Golden_2_Train, \
            Apple_Golden_3_Train, Apple_Crimson_Snow_Test, Apple_Golden_1_Test, \
            Apple_Golden_2_Test, Apple_Golden_3_Test, batch_size, img_height, img_width, \
            trainpath, testpath, num_classes, CNNClassifier
        CNNClassifier = f"{fruits}\\CNNClassifier.h5"
        trainpath = f"{fruits}\\fruits-360-5\\Training"
        testpath = f"{fruits}\\fruits-360-5\\Test"
        Apple_Braeburn_Train = f"{trainpath}\\Apple Braeburn"
        Apple_Crimson_Snow_Train = f"{trainpath}\\Apple Crimson Snow"
        Apple_Golden_1_Train = f"{trainpath}\\Apple Golden 1"
        Apple_Golden_2_Train = f"{trainpath}\\Apple Golden 2"
        Apple_Golden_3_Train = f"{trainpath}\\Apple Golden 3"
        Apple_Braeburn_Test = f"{testpath}\\Apple Braeburn"
        Apple_Crimson_Snow_Test = f"{testpath}\\Apple Crimson Snow"
        Apple_Golden_1_Test = f"{testpath}\\Apple Golden 1"
        Apple_Golden_2_Test = f"{testpath}\\Apple Golden 2"
        Apple_Golden_3_Test = f"{testpath}\\Apple Golden 3"
        batch_size = 32
        img_height = 100
        img_width = 100
        num_classes = 5  # 레이블 값의 개수, 즉 사과 품종의 개수

    def hook(self):
        # self.show_apple()
        train_ds = self.create_train_ds()
        class_names = train_ds.class_names
        train_ds = self.change_to_prefetch_with_shuffle(train_ds)
        val_ds = self.create_validation_ds()
        val_ds = self.change_to_prefetch(val_ds)
        test_ds = self.create_test_ds()
        test_ds1 = self.create_test_ds1()
        self.merge_image_label_tester(test_ds=test_ds,
                                      test_ds1=test_ds1,
                                      class_names=class_names,
                                      index=-1)  # -1 은 가장 마지막 인덱스
        if not os.path.isfile(CNNClassifier):
            model = self.create_model(train_ds=train_ds,val_ds=val_ds)
        else:
            model = load_model(CNNClassifier)
        print(f"model.summary(): \n{model.summary()}")


    def show_apple(self):
        img = tf.keras.preprocessing.image.load_img \
            (f'{Apple_Golden_3_Train}\\0_100.jpg')
        plt.imshow(img)
        plt.axis("off")
        plt.show()

    def create_train_ds(self):
        return tf.keras.preprocessing.image_dataset_from_directory(
            trainpath,
            validation_split=0.3,
            subset="training",
            seed=1,
            image_size=(img_height, img_width),
            batch_size=batch_size)

    def create_validation_ds(self):
        return tf.keras.preprocessing.image_dataset_from_directory(
            trainpath,
            validation_split=0.3,
            subset="validation",
            seed=1,
            image_size=(img_height, img_width),
            batch_size=batch_size)

    def create_test_ds(self):
        test_ds = tf.keras.preprocessing.image_dataset_from_directory(
            testpath,
            seed=1,
            image_size=(img_height, img_width),
            batch_size=batch_size)
        print(f"*** Type of test_ds is {type(test_ds)} ***")
        # Type of test_ds is tensorflow.python.data.ops.dataset_ops.BatchDataset
        return test_ds

    def create_test_ds1(self):
        return tf.keras.preprocessing.image_dataset_from_directory(
            testpath,
            seed=1,
            image_size=(img_height, img_width),
            batch_size=batch_size,
            shuffle=False)  # shuffle=False 데이터셋 test_ds1을 별도로 생성

    def extract_label_from_ds(self, ds):
        return np.concatenate([y for x, y in ds], axis=0)

    def extract_image_info(self, ds):
        return np.concatenate([x for x, y in ds], axis=0)

    def merge_image_label_tester(self, **kwargs):
        test_ds = kwargs["test_ds"]
        test_ds1 = kwargs["test_ds1"]
        class_names = kwargs["class_names"]
        y = self.extract_label_from_ds(test_ds)
        print(f"test_ds에서 레이블 정보만 추출하여 y에 저장\n"
              f"실행할 때마다 y 배열이 변경됨: {y}\n")
        y = self.extract_label_from_ds(test_ds1)
        print(f"Shuffle=False 옵션을 통해 불러온 test_ds1 정보를 y에 저장\n"
              f"실행할 때마다 y 배열이 변경이 없음: {y}\n")
        x = self.extract_image_info(kwargs["test_ds1"])
        print(f"test_ds1에서 이미지 정보만 추출하여 x에 저장 : {x[0]}\n")
        plt.figure(figsize=(3, 3))
        plt.imshow(x[0].astype("uint8"))
        plt.title(class_names[y[0]])
        plt.axis("off")
        plt.show()

    def merge_image_label(self, **kwargs):
        dataset = kwargs["dataset"]
        class_names = kwargs["class_names"]
        i = kwargs["index"]
        x = self.extract_image_info(dataset)
        y = self.extract_label_from_ds(dataset)
        plt.figure(figsize=(3, 3))
        plt.imshow(x[i].astype("uint8"))
        plt.title(class_names[y[i]])
        plt.axis("off")
        plt.show()

    def change_to_prefetch(self, dataset):
        # train_ds 데이터셋을 Prefetch 데이터셋으로 설정
        AUTOTUNE = tf.data.experimental.AUTOTUNE
        prefetch_dataset = dataset.cache().prefetch(buffer_size=AUTOTUNE)
        return prefetch_dataset

    def change_to_prefetch_with_shuffle(self, dataset):
        # test_ds, val_ds 데이터셋을 Prefetch 데이터셋으로 설정
        BUFFER_SIZE = 10000
        AUTOTUNE = tf.data.experimental.AUTOTUNE
        prefetch_dataset = dataset.cache().shuffle(BUFFER_SIZE).prefetch(buffer_size=AUTOTUNE)
        type(f"Type of train_ds is {prefetch_dataset}")
        '''Type of train_ds is tensorflow.python.data.ops.dataset_ops.PrefetchDataset'''
        return prefetch_dataset

    def create_model(self, **kwargs):
        train_ds = kwargs["train_ds"]
        val_ds = kwargs["val_ds"]
        model = tf.keras.Sequential([
            keras.layers.experimental.preprocessing.Rescaling(1. / 255, input_shape=(img_height, img_width, 3)),
            layers.Conv2D(16, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(2),
            layers.Dropout(.50),
            layers.Conv2D(32, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(2),
            layers.Dropout(.50),
            layers.Flatten(),
            layers.Dense(500, activation='relu'),
            layers.Dropout(.50),
            layers.Dense(num_classes, activation='softmax')
        ])
        model.compile(
            optimizer='adam',
            loss=tf.losses.SparseCategoricalCrossentropy(),
            metrics=['accuracy'])
        checkpointer = ModelCheckpoint(f"{fruits}\\CNNClassifier.h5", save_best_only=True)
        early_stopping_cb = keras.callbacks.EarlyStopping(patience=5, monitor='val_accuracy',
                                                          restore_best_weights=True)
        epochs = 20

        history = model.fit(
            train_ds,
            batch_size=batch_size,
            validation_data=val_ds,
            epochs=epochs,
            callbacks=[checkpointer, early_stopping_cb]
        )
        print(f"len(history.history['val_accuracy']) is {len(history.history['val_accuracy'])}")
        # 매 epochs마다 모델 정확도와 손실을 그래프로 그리기

        acc = history.history['accuracy']  # 모델의 학습 정확도를 변수 acc에 저장
        val_acc = history.history['val_accuracy']  # 모델의 검증 정확도를 변수 val_acc에 저장

        loss = history.history['loss']  # 모델의 학습 손실을 변수 loss에 저장
        val_loss = history.history['val_loss']  # 모델의 검증 손실을 변수 val_loss에 저장

        # epochs가 14회가 아닌 다른 결과(예:10회)로 나오면 아래 줄 14를 해당 숫자인 10로 바꿔주야 함에 유의
        epochs_range = range(1, len(loss) + 1)  # epochs가 14회까지만 수행된 것을 반영
        # len(history.history['val_accuracy']) is 11

        # 학습 정확도와 검증 정확도를 그리기
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, acc, label='Training Accuracy')
        plt.plot(epochs_range, val_acc, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.title('Training and Validation Accuracy')

        # 학습 손실와 검증 손실을 그리기
        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, loss, label='Training Loss')
        plt.plot(epochs_range, val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.title('Training and Validation Loss')
        plt.show()
        return model


