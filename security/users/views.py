from django.http import JsonResponse
from matplotlib import pyplot as plt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from security.users.seivice import UserService


@api_view(['POST'])
@parser_classes([JSONParser])
def user_list(request):
    service = UserService()
    service.get_users()
    return JsonResponse({'users': UserService().get_users()})

def login(request):
    pass