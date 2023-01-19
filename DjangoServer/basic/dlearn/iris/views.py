from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
import tensorflow as tf

from basic.dlearn.iris.services import IrisService

'''
아이리스 품종 3: setosa, versicolor, virginica
'SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm'
꽃받침 길이, 꽃받침 너비, 꽃잎 길이, 꽃잎 너비

QueryDict 관련 블로그
https://velog.io/@qlgks1/Django-request-HttpRequest-QueryDict
'''
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
    print(f'Result Type: {type(result)}')
    print(result)
    if result == 0:
        resp = 'setosa / 부채붓꽃'
    elif result == 1:
        resp = 'versicolor / 버시칼라'
    elif result == 2:
        resp = 'virginica / 버지니카'
    print(f' 붓꽃 is {resp}')
    return JsonResponse({'result':resp})