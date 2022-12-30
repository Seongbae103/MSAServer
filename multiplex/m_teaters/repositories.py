from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import JsonResponse
from rest_framework.response import Response

from multiplex.m_teaters.models import M_theater
from multiplex.m_teaters.serializer import M_theaterSerializer


# DAO
class M_theaterRepository(object):
    def get_all(self):
        return Response(M_theaterSerializer(M_theater.objects.all(), many=True).data)

    def find_by_id(self):
        return Response(M_theaterSerializer(M_theater.objects.all(), many=True).data)
