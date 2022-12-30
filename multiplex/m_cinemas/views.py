from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from multiplex.m_cinemas.repositories import M_cinemaRepository
from multiplex.m_cinemas.serializer import M_cinemaSerializer

@api_view(['POST', 'PUT', 'PETCH', 'DELETE', 'GET'])
@parser_classes([JSONParser])
def cinema(request):
    if request.method == "POST":
        return M_cinemaSerializer().create(request.data)
    elif request.method == 'PUT':
        return M_cinemaSerializer().update(request.data)
    elif request.method == 'PETCH':
        return None
    elif request.method == 'DELETE':
        return M_cinemaSerializer().delete(request.data)
    elif request.method == 'GET':
        return M_cinemaRepository().find_cinema_by_id(request.data)

@api_view(['GET'])
@parser_classes([JSONParser])
def cinema_list(request): return M_cinemaRepository().get_all(request.data) #안에 다른 파라미터는 필요없지만 paga number는 들어갈 수 있다