from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from shop.iris.Iris_Model import Iris


@api_view(['POST'])
@parser_classes([JSONParser])
def iris(request):

    print(f'Enter Blog-Login with {request}')
    return JsonResponse({'Response Test ': 'SUCCESS'})