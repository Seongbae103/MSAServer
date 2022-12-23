from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from blog.b_users.service import UserService


@api_view(['GET'])
@parser_classes([JSONParser])
def signup(request):

    return JsonResponse({'로그인 결과 ': UserService().getusers()})