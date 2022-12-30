from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from security.users.repositories import UserRepository
from security.users.serializer import UserSerializer



@api_view(['POST', 'PUT', 'PETCH', 'DELETE', 'GET'])
@parser_classes([JSONParser])
def user(request):
    if request.method == "POST":
        new_user = request.data
        print(f" 리액트에서 등록한 신규 사용자 {new_user}")
        serilalizer = UserSerializer(data=new_user)
        if serilalizer.is_valid():
            serilalizer.save()
            return JsonResponse({"result":"SUCCESS"})
        return JsonResponse(serilalizer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        repo = UserRepository()
        modify_user = repo.find_user_by_email(request.data["user_email"])
        db_user = repo.find_by_id(modify_user.id)
        serializer = UserSerializer(data=db_user)
        if serializer.is_valid():
            serializer.update(modify_user, db_user)
            return JsonResponse({"result": "SUCCESS"})
    elif request.method == 'PETCH':
        return None
    elif request.method == 'DELETE':
        repo = UserRepository()
        delete_user = repo.find_user_by_email(request.data["user_email"])
        db_user = repo.find_by_id(delete_user.id)
        db_user.delete()
        return JsonResponse({"result": "SUCCESS"})
    elif request.method == 'GET':
        return Response(UserRepository().find_user_by_email(request.data["user_email"]))



@api_view(['GET'])
@parser_classes([JSONParser])#안에 다른 파라미터는 필요없지만 paga number는 들어갈 수 있다
def user_list(request): return UserRepository().get_all()

@api_view(['POST'])
@parser_classes([JSONParser])
def login(request):
    return UserRepository().login(request.data)  # dictionary이외를 받을 경우, 두번째 argument를 safe=False로 설정해야한다.

@api_view(['GET'])
@parser_classes([JSONParser])
def user_list_by_name(request):
    return UserRepository().find_users_by_name(request.data["user_name"])