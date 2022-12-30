from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from shop.s_products.serializer import S_productSerializer

@api_view(['POST', 'PUT', 'PETCH', 'DELETE', 'GET'])
@parser_classes([JSONParser])
def product(request):
    if request.method == "POST":
        return S_productSerializer().create(request.data)
    elif request.method =='PUT':
        return S_productSerializer().update(request.data)
    elif request.method =='PETCH':
        return None
    elif request.method =='DELETE':
        return S_productSerializer().delete(request.data)
    elif request.method =='GET':
        return S_productSerializer().find_product_by_id(request.data)

@api_view(['GET'])
@parser_classes([JSONParser])
def user_list(request): return S_productSerializer().get_all(request.data) #안에 다른 파라미터는 필요없지만 paga number는 들어갈 수 있다

