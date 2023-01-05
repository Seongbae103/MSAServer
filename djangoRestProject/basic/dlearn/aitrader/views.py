from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from basic.dlearn.aitrader.services import AiTraderService


@api_view(['POST'])
@parser_classes([JSONParser])
def samsungtrader(request):
    result = AiTraderService().service_model()
    print(f'결과: {result}')

    return JsonResponse({'결과': result})

