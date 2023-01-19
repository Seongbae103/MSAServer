from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def test(request):
    print(" ### Server Started ! ### ")
    return Response({'message': "Server Started !"})