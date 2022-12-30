from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from shop.s_deliveries.serializer import S_deliverySerializer

@api_view(['POST', 'PUT', 'PETCH', 'DELETE', 'GET'])
@parser_classes([JSONParser])
def delivery(request):
    if request.method == "POST":
        return S_deliverySerializer().create(request.data)
    elif request.method =='PUT':
        return S_deliverySerializer().update(request.data)
    elif request.method =='PETCH':
        return None
    elif request.method =='DELETE':
        return S_deliverySerializer().delete(request.data)
    elif request.method =='GET':
        return S_deliverySerializer().find_delivery_by_id(request.data)


@api_view(['GET'])
@parser_classes([JSONParser])
def delivery_list(request): return S_deliverySerializer().get_all(request.data) #안에 다른 파라미터는 필요없지만 paga number는 들어갈 수 있다

