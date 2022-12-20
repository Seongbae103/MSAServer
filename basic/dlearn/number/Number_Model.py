import tensorflow as tf
from keras.models import load_model
from matplotlib import pyplot as plt


class FashionModel(object):

    def hook(self):
        self.create_model()

    def create_model(self): #분류 (회기시는 모양이 다르다)
        mnist = tf.keras.datasets.mnist
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        x_train, x_test = x_train / 255.0, x_test / 255.0
        model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(512, activation=tf.nn.relu),
            tf.keras.layers.Dense(10, activation=tf.nn.softmax)
        ])
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        model.fit(x_train, y_train, epochs=5)
        test_loss, test_acc = model.evaluate(x_test, y_test)
        print('테스트 정확도:', test_acc)
        file_name = r"/basic/dlearn/save\number_model.h5"
        print(f'저장경로: {file_name}')
        model.save(file_name)

MODEL_MENUS = ["종료", #0
            "데이터구조파악",
            "전체 실행"]

model_menu = {
    "1" : lambda t : t.hook()
}

if __name__ == '__main__':

    t = FashionModel()
    while True:
        [print(f"{i}. {j}") for i, j in enumerate(model_menu)]
        menu = input('메뉴선택: ')
        if menu == 0:
            print("종료")
            break
        else:
            try:
                model_menu[menu](t)
            except KeyError as e:
                if 'some error message' in str(e):
                    print('Caught error message')
                else:
                    print("Didn't catch error message")
