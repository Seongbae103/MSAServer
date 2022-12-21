from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from basic.webcrawler.naver_movie.Services import ScrapService


@api_view(['GET'])
@parser_classes([JSONParser])
def navermovie(request):
    if request.method == 'GET':
        return JsonResponse(
            {'result': ScrapService().naver_movie_review()})
    else:
        print(f"######## ID is None ########")