from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from multiplex.m_teaters.repositories import M_theaterRepository
from multiplex.m_teaters.serializer import M_theaterSerializer

@api_view(['POST', 'PUT', 'PETCH', 'DELETE', 'GET'])
@parser_classes([JSONParser])
def teater(request):
    if request.method == "POST":
        return M_theaterSerializer().create(request.data)
    elif request.method == 'PUT':
        return M_theaterSerializer().update(request.data)
    elif request.method == 'PETCH':
        return None
    elif request.method == 'DELETE':
        return M_theaterSerializer().delete(request.data)
    elif request.method == 'GET':
        return M_theaterRepository().find_teater_by_id(request.data)

@api_view(['GET'])
@parser_classes([JSONParser])
def teater_list(request): return M_theaterRepository().get_all(request.data) #안에 다른 파라미터는 필요없지만 paga number는 들어갈 수 있다