import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from shop.Fashion_Service import FashionService

''' 디버그용
plt.subplot(1, 2, 2)
    service.plot_value_array(test_num, predictions, test_labels)
    plt.show()
'''
@api_view(['GET', 'POST'])
def fashion(request):
    if request.method == 'GET':
        print(f"######## ID is {request.GET['id']} ########")
        return JsonResponse(
            {'result': FashionService().service_model(int(request.GET['id']))})
    elif request.method == 'POST':
        data = json.loads(request.body)  # json to dict
        print(f"######## ID is {data['id']} ########")
        return JsonResponse({'result': FashionService().service_model(int(data['id']))})