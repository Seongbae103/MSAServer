from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from basic.nlp.imdb.services import NaverMovieService


@api_view(['POST'])
@parser_classes([JSONParser])
def korean_classify_view(request):
    review = request.data
    print(f"******** 리액트에서 넘어온 리뷰 : {review} ******** ")
    result = NaverMovieService().process(review["inputs"])
    print(f'긍정률: {result}')

    return JsonResponse({'result': result})