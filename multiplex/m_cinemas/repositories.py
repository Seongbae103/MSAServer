from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import JsonResponse
from rest_framework.response import Response

from multiplex.m_cinemas.models import M_cinema
from multiplex.m_cinemas.serializer import M_cinemaSerializer


# DAO
class M_cinemaRepository(object):
    def get_all(self):
        return Response(M_cinemaSerializer(M_cinema.objects.all(), many=True).data)

    def find_by_id(self):
        return Response(M_cinemaSerializer(M_cinema.objects.all(), many=True).data)

    def login(self, kwargs):
        loginUser = M_cinema.objects.get(user_email=kwargs["user_email"])
        print(f"해당 email 을 가진  User ID: *** \n {loginUser.id}")
        if loginUser.password == kwargs["password"]:
            dbUser = M_cinema.objects.all().filter(id=loginUser.id).values()[0]
            print(f" DBUser is {dbUser}")
            serializer = M_cinemaSerializer(loginUser, many=False)
            return JsonResponse(data=serializer.data,
                                safe=False)  # == return JsonResponse({"data":serializer.data, "safe":False})
        else:
            return JsonResponse({"data" : "WRONG_PASSWORD"}) #JsonResponse가 리액트로 보내주는 DTO

