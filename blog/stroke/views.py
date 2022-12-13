from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from blog.stroke.Stroke import StrokeService

@api_view(['GET'])
@parser_classes([JSONParser])
def stroke(request):
    StrokeService().hook()
    print(f'Enter Blog-Login with {request}')
    return JsonResponse({'Response Test ': 'SUCCESS'})