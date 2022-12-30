from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from shop.s_categories.serializer import S_categorySerializer

@api_view(['POST', 'PUT', 'PETCH', 'DELETE', 'GET'])
@parser_classes([JSONParser])
def category(request):
    if request.method == "POST":
        return S_categorySerializer().create(request.data)
    elif request.method =='PUT':
        return S_categorySerializer().update(request.data)
    elif request.method =='PETCH':
        return None
    elif request.method =='DELETE':
        return S_categorySerializer().delete(request.data)
    elif request.method =='GET':
        return S_categorySerializer().find_category_by_id(request.data)

@api_view(['GET'])
@parser_classes([JSONParser])
def category_list(request): return S_categorySerializer().get_all(request.data) #안에 다른 파라미터는 필요없지만 paga number는 들어갈 수 있다
