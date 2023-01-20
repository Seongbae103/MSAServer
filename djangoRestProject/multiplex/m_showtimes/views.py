from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from multiplex.m_showtimes.repositories import M_showtimeRepository
from multiplex.m_showtimes.serializer import M_showtimeSerializer

@api_view(['POST', 'PUT', 'PETCH', 'DELETE', 'GET'])
@parser_classes([JSONParser])
def show_time(request):
    if request.method == "POST":
        return M_showtimeSerializer().create(request.data)
    elif request.method == 'PUT':
        return M_showtimeSerializer().update(request.data)
    elif request.method == 'PETCH':
        return None
    elif request.method == 'DELETE':
        return M_showtimeSerializer().delete(request.data)
    elif request.method == 'GET':
        return M_showtimeRepository().find_teater_ticket_by_id(request.data)

@api_view(['GET'])
@parser_classes([JSONParser])
def show_time_list(request): return M_showtimeRepository().get_all(request.data) #안에 다른 파라미터는 필요없지만 paga number는 들어갈 수 있다