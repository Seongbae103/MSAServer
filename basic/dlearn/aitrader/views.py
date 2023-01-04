from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from basic.dlearn.aitrader.samsung_trader_dnn_model import SamsungTrader



@api_view(['POST'])
@parser_classes([JSONParser])
def samsungtrader(request):
    result = SamsungTrader().hook()
    print(f'결과: {result}')

    return JsonResponse({'결과': result})

