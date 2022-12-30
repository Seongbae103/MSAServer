from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from blog.b_comments.serializer import B_commentSerializer

@api_view(['POST', 'PUT', 'PETCH', 'DELETE', 'GET'])
@parser_classes([JSONParser])
def comment(request):
    if request.method == "POST":
        return B_commentSerializer().create(request.data)
    elif request.method == 'PUT':
        return B_commentSerializer().update(request.data)
    elif request.method == 'PETCH':
        return None
    elif request.method == 'DELETE':
        return B_commentSerializer().delete(request.data)
    elif request.method == 'GET':
        return B_commentSerializer().find_comment_by_id(request.data)

@api_view(['GET'])
@parser_classes([JSONParser])
def comment_list(request): return B_commentSerializer().get_all(request.data) #안에 다른 파라미터는 필요없지만 paga number는 들어갈 수 있다