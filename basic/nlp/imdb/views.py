from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from basic.nlp.imdb.services import NaverMovieService


@api_view(['POST'])
@parser_classes([JSONParser])
def navermovie(request):
    result = NaverMovieService().process(request.data['inputs'])
    print(f'긍정률: {result}')

    return JsonResponse({'긍정률': result})

