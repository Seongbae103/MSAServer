from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from security.users.models import User
from security.users.repositories import UserRepository
from security.users.serializers import UserSerializer


@api_view(['POST','PUT','PATCH','DELETE','GET'])
@parser_classes([JSONParser])
def user(request):
    if request.method == "POST":
        new_user = request.data
        print(f" 리액트에서 등록한 신규 사용자 {new_user}")
        serializer = UserSerializer(data=new_user)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"result": "SUCCESS"})
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET":
        return Response(UserRepository()
                        .find_user_by_email(request
                                            .data["user_email"]))
    elif request.method == "PATCH":
        return None
    elif request.method == "PUT":
        repo = UserRepository()
        modify_user = repo.find_user_by_email(request.data["user_email"])
        db_user = repo.find_by_id(modify_user.id)
        serializer = UserSerializer(data=db_user)
        if serializer.is_valid():
            serializer.update(modify_user, db_user)
            return JsonResponse({"result": "SUCCESS"})
    elif request.method == "DELETE":
        repo = UserRepository()
        delete_user = repo.find_user_by_email(request.data["user_email"])
        db_user = repo.find_by_id(delete_user.id)
        db_user.delete()
        return JsonResponse({"result": "SUCCESS"})


@api_view(['GET'])
@parser_classes([JSONParser])
def user_list(request): return UserRepository().get_all()

@api_view(['POST'])
@parser_classes([JSONParser])
def login(request): return UserRepository().login(request.data)

@api_view(['GET'])
@parser_classes([JSONParser])
def user_list_by_name(request):
    return UserRepository().find_users_by_name(request.data["user_name"])

@api_view(['GET'])
@parser_classes([JSONParser])
def exist_email(request, email):
    exist = User.objects.all().filter(user_email=email).values()[0]
    if not email == exist['user_email']:
        return JsonResponse({"result":"SUCCESS"})

'''
iss: 토큰 발급자 (issuer)
sub: 토큰 제목 (subject)
aud: 토큰 대상자 (audience)
exp: 토큰의 만료시간 (expiraton), 시간은 NumericDate 형식으로 되어있어야 하며 (예: 1480849147370) 언제나 현재 시간보다 이후로 설정되어있어야합니다.
nbf: Not Before 를 의미하며, 토큰의 활성 날짜와 비슷한 개념입니다. 여기에도 NumericDate 형식으로 날짜를 지정하며, 이 날짜가 지나기 전까지는 토큰이 처리되지 않습니다.
iat: 토큰이 발급된 시간 (issued at), 이 값을 사용하여 토큰의 age 가 얼마나 되었는지 판단 할 수 있습니다.
jti: JWT의 고유 식별자로서, 주로 중복적인 처리를 방지하기 위하여 사용됩니다. 일회용 토큰에 사용하면 유용합니다.
'''

'''
# Header ############################
{
    "alg": "HS256",
    "typ": "JWT"
}

# Payload ###########################
{
    "sub": "1234567890",
    "name": "John Doe",
    "iat": 1516239022
}

# Signature #########################
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)
'''