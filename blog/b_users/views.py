from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from blog.b_users.repositories import B_userRepository
from blog.b_users.serializer import B_userSerializer

@api_view(['POST', 'PUT', 'PETCH', 'DELETE', 'GET'])
@parser_classes([JSONParser])
def user(request):
    if request.method == "POST":
        return B_userSerializer().create(request.data)
    elif request.method == 'PUT':
        return B_userSerializer().update(request.data)
    elif request.method == 'PETCH':
        return None
    elif request.method == 'DELETE':
        return B_userSerializer().delete(request.data)
    elif request.method == 'GET':
        return B_userRepository().find_user_by_id(request.data)

@api_view(['GET'])
@parser_classes([JSONParser])
def user_list(request): return B_userRepository().get_all(request.data) #안에 다른 파라미터는 필요없지만 paga number는 들어갈 수 있다