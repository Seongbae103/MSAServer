from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from basic.nlp.korean_classify.services import KoreanClassifyServices


@api_view(['POST'])
@parser_classes([JSONParser])
def korean_classify(request):
    result = KoreanClassifyServices().hook()
    print(f'결과: {result}')

    return JsonResponse({'결과': result})

