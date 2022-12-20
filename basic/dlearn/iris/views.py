from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
import tensorflow as tf
from basic.dlearn.iris.Iris_Service import IrisService


@api_view(['POST'])
@parser_classes([JSONParser])
def iris(request):
    iris_data = request.data
    print(f'리액트에서 보낸 데이터: {request.data}')
    SepalLengthCm = tf.constant(float(iris_data['SepalLengthCm']))
    SepalWidthCm = tf.constant(float(iris_data['SepalWidthCm']))
    PetalLengthCm = tf.constant(float(iris_data['PetalLengthCm']))
    PetalWidthCm = tf.constant(float(iris_data['PetalWidthCm']))
    print(f'리액트에서 보낸 데이터 : {iris_data}')
    print(f'꽃받침의 길이 : {SepalLengthCm}')
    print(f'꽃받침의 너비 : {SepalWidthCm}')
    print(f'꽃잎의 길이: {PetalLengthCm}')
    print(f'꽃잎의 너비 : {PetalWidthCm}')
    result = IrisService().service_model([SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm])
    print(f'찾는 품종: {result}')
    if result == 0:
        print('setosa / 부채붓꽃')
    elif result == 1:
        print('versicolor / 버시칼라 ')
    elif result == 2:
        print('virginica / 버지니카')
    return JsonResponse({'result': result})
