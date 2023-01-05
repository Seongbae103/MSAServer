import json
from django.http import JsonResponse
from matplotlib import pyplot as plt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from basic.dlearn.number.Number_Service import NumberService

''' 디버그용
plt.subplot(1, 2, 2)
    service.plot_value_array(test_num, predictions, test_labels)
    plt.show()
'''
@api_view(['POST', 'GET'])
@parser_classes([JSONParser])
def number(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # json to dict
        a = NumberService().service_model(int(data['id']))
        print(f" 리턴결과 : {a} ")
        plt.figure()
        plt.grid(False)
        plt.show()
        return JsonResponse({'result': a})

    elif request.method == 'GET':
        plt.figure()
        plt.grid(False)
        plt.show()
        return JsonResponse(
            {'result': NumberService().service_model(int(request.GET['id']))})
    else:
        print(f"######## ID is None ########")