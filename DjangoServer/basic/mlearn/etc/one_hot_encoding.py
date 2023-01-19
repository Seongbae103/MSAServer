import tensorflow as tf
import numpy as np

#2. 학습에 사용할 데이터 정의 => 털, 날개: 있으면 1 없으면 0
#[털, 날개]
x_data = np.array(
	[[0,0], [1,0], [0,0], [0,0], [0,1]]) #원-핫 인코딩

#판별 개체 종류 => 기타, 포유류, 조류
#기타 = [1,0,0]
#포유류 = [0,1,0]
#조류 = [0,0,1]

#실측값 데이터 정의 => 레이블 데이터 (Ground Truth, GT라고도 함. 정답지라는 뜻)
y_data = np.array([
	[1,0,0], #기타
    [0,1,0], #포유류
    [0,0,1], #조류
    [1,0,0],
    [1,0,0],
    [0,0,1]
])

'''
x, y 간 상관관계
[0,0] => [1,0,0] / 털X, 날개X: 기타
[1,0] => [0,1,0] / 털O, 날개X: 포유류
[0,1] => [0,1,0] / 털X, 날개O: 조류
[1,1] => [0,0,1] / 털O, 날개O: 조류
'''
model = tf.keras.models.Sequential([
	tf.keras.layers.Dense(3, activation = 'relu', kernel_initializer='random_uniform', bias_initializer='zeros'),
    tf.keras.layers.Dense(3, activation = 'softmax')
])
model.compile(optimizer = 'SGD',
	loss = 'categorical_crossentropy',
    metrics=['accuracy'])

#모델 학습
model.fit(x_data, y_data, epochs=1000)