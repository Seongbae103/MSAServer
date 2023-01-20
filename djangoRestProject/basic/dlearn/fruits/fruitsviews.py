
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from basic.dlearn.fashion.Fashion_Service import FashionService

@api_view(['GET'])
@parser_classes([JSONParser])
def fruits(request):
    if request.method == 'GET':
        return JsonResponse(
            {'result': FashionService().service_model(int(request.GET['id']))})

    else:
        print(f"######## ID is None ########")