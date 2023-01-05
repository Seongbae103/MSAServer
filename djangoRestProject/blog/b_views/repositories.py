from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import JsonResponse
from rest_framework.response import Response

from blog.b_views.models import B_view
from blog.b_views.serializer import B_viewSerializer


# DAO
class B_viewRepository(object):
    def get_all(self):
        return Response(B_viewSerializer(B_view.objects.all(), many=True).data)

    def find_by_id(self):
        return Response(B_viewSerializer(B_view.objects.all(), many=True).data)
