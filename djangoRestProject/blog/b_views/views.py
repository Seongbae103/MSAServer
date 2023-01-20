from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from blog.b_views.repositories import B_viewRepository
from blog.b_views.serializer import B_viewSerializer

@api_view(['POST', 'PUT', 'PETCH', 'DELETE', 'GET'])
@parser_classes([JSONParser])
def view(request):
    if request.method == "POST":
        return B_viewSerializer().create(request.data)
    elif request.method == 'PUT':
        return B_viewSerializer().update(request.data)
    elif request.method == 'PETCH':
        return None
    elif request.method == 'DELETE':
        return B_viewSerializer().delete(request.data)
    elif request.method == 'GET':
        return B_viewRepository().find_view_by_id(request.data)

@api_view(['GET'])
@parser_classes([JSONParser])
def view_list(request): return B_viewRepository().get_all(request.data) #안에 다른 파라미터는 필요없지만 paga number는 들어갈 수 있다