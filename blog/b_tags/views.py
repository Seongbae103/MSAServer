from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from blog.b_tags.repositories import B_tagRepository
from blog.b_tags.serializer import B_tagSerializer

@api_view(['POST', 'PUT', 'PETCH', 'DELETE', 'GET'])
@parser_classes([JSONParser])
def tag(request):
    if request.method == "POST":
        return B_tagSerializer().create(request.data)
    elif request.method == 'PUT':
        return B_tagSerializer().update(request.data)
    elif request.method == 'PETCH':
        return None
    elif request.method == 'DELETE':
        return B_tagSerializer().delete(request.data)
    elif request.method == 'GET':
        return B_tagRepository().find_tag_by_id(request.data)

@api_view(['GET'])
@parser_classes([JSONParser])
def tag_list(request): return B_tagRepository().get_all(request.data) #안에 다른 파라미터는 필요없지만 paga number는 들어갈 수 있다

