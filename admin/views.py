from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def hello(request):
    print('####### admin/views #########')
    return Response({'manage: "server Started !'})