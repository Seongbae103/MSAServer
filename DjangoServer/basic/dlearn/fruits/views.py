from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from basic.dlearn.fruits.services import FruitsService

@api_view(['GET'])
@parser_classes([JSONParser])
def fruits(request):
    return JsonResponse(
        {'result': FruitsService().find_fruits(int(request.GET['id']))})


