from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from blog.b_posts.repositories import B_postRepository
from blog.b_posts.serializer import B_postSerializer

@api_view(['POST', 'PUT', 'PETCH', 'DELETE', 'GET'])
@parser_classes([JSONParser])
def post(request):
    if request.method == "POST":
        return B_postSerializer().create(request.data)
    elif request.method == 'PUT':
        return B_postSerializer().update(request.data)
    elif request.method == 'PETCH':
        return None
    elif request.method == 'DELETE':
        return B_postSerializer().delete(request.data)
    elif request.method == 'GET':
        return B_postRepository().find_post_by_id(request.data)

@api_view(['GET'])
@parser_classes([JSONParser])
def post_list(request): return B_postRepository().get_all(request.data) #안에 다른 파라미터는 필요없지만 paga number는 들어갈 수 있다