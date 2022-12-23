import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from basic.dlearn.fashion.Fashion_Service import FashionService

''' 디버그용
plt.subplot(1, 2, 2)
    service.plot_value_array(test_num, predictions, test_labels)
    plt.show()
'''
@api_view(['POST', 'GET'])
@parser_classes([JSONParser])
def fashion(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # json to dict
        a = FashionService().service_model(int(data['id']))
        print(f" 리턴결과 : {a} ")
        return JsonResponse({'result': a})
    elif request.method == 'GET':
        return JsonResponse(
            {'result': FashionService().service_model(int(request.GET['id']))})

        """
        fruits-360-5 = request.fruits-360-5
        test_num = tf.constant(int(fruits-360-5['test_num']))
        result = FashionService().service_model([test_num])
        return JsonResponse({'result': result})
        """

    else:
        print(f"######## ID is None ########")