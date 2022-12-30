from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from multiplex.m_teater_tickets.repositories import M_theaterTicketRepository
from multiplex.m_teater_tickets.serializer import M_theaterTicketSerializer

@api_view(['POST', 'PUT', 'PETCH', 'DELETE', 'GET'])
@parser_classes([JSONParser])
def teater_ticket(request):
    if request.method == "POST":
        return M_theaterTicketSerializer().create(request.data)
    elif request.method == 'PUT':
        return M_theaterTicketSerializer().update(request.data)
    elif request.method == 'PETCH':
        return None
    elif request.method == 'DELETE':
        return M_theaterTicketSerializer().delete(request.data)
    elif request.method == 'GET':
        return M_theaterTicketRepository().find_teater_ticket_by_id(request.data)

@api_view(['GET'])
@parser_classes([JSONParser])
def teater_ticket_list(request): return M_theaterTicketRepository().get_all(request.data) #안에 다른 파라미터는 필요없지만 paga number는 들어갈 수 있다