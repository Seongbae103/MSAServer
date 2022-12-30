from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from shop.s_carts.serializer import S_cartSerializer

@api_view(['POST', 'PUT', 'PETCH', 'DELETE', 'GET'])
@parser_classes([JSONParser])
def cart(request):
    if request.method == "POST":
        return S_cartSerializer().create(request.data)
    elif request.method =='PUT':
        return S_cartSerializer().update(request.data)
    elif request.method =='PETCH':
        return None
    elif request.method =='DELETE':
        return S_cartSerializer().delete(request.data)
    elif request.method =='GET':
        return S_cartSerializer().find_cart_by_id(request.data)

@api_view(['GET'])
@parser_classes([JSONParser])
def cart_list(request): return S_cartSerializer().get_all(request.data) #안에 다른 파라미터는 필요없지만 paga number는 들어갈 수 있다
