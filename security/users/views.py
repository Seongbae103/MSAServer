from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from security.users.models import User
from security.users.serializer import UserSerializer
from rest_framework.response import Response

@api_view(['GET'])
@parser_classes([JSONParser])
def user_list(request):
    if request.method == "GET":
        #service = UserService()
        serializer = UserSerializer(User.objects.all(), many=True)    # 1. '''UserSerializer(model의 클래스명.objects.all())'''
        return Response(serializer.data)                                   # 2. return JsonResponse({'users': serializer.data})에서 바로 serializer만 호출하면 가방에 펜 넣고 글쓰기

@api_view(['POST'])
@parser_classes([JSONParser])
def user_login(request):
    print(f"로그인 정보 : {request.data}")
    loginInfo = request.data
    loginUser = User.objects.get(user_email=loginInfo["user_email"])
    print(f"해당 email 을 가진  User ID: *** \n {loginUser.id}")
    if loginUser.password == loginInfo["password"]:
        dbUser = User.objects.all().filter(id=loginUser.id).values()[0]
        print(f" DBUser is {dbUser}")
        serializer = UserSerializer(loginUser, many=False)
        return JsonResponse(data=serializer.data,
                            safe=False)  # == return JsonResponse({"data":serializer.data, "safe":False})

        # dictionary이외를 받을 경우, 두번째 argument를 safe=False로 설정해야한다.
