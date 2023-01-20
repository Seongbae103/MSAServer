from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import JsonResponse
from rest_framework.response import Response

from multiplex.m_users.models import M_user
from multiplex.m_users.serializer import M_userSerializer


# DAO
class M_userRepository(object):
    def get_all(self):
        return Response(M_userSerializer(M_user.objects.all(), many=True).data)

    def find_user_by_id(self):
        return Response(M_userSerializer(M_user.objects.all(), many=True).data)

    def login(self, kwargs):
        loginUser = M_user.objects.get(user_email=kwargs["user_email"])
        print(f"해당 email 을 가진  User ID: *** \n {loginUser.id}")
        if loginUser.password == kwargs["password"]:
            dbUser = M_user.objects.all().filter(id=loginUser.id).values()[0]
            print(f" DBUser is {dbUser}")
            serializer = M_userSerializer(loginUser, many=False)
            return JsonResponse(data=serializer.data,
                                safe=False)  # == return JsonResponse({"data":serializer.data, "safe":False})
        else:
            return JsonResponse({"data" : "WRONG_PASSWORD"}) #JsonResponse가 리액트로 보내주는 DTO

