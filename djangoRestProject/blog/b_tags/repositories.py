from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import JsonResponse
from rest_framework.response import Response

from blog.b_tags.models import B_tag
from blog.b_tags.serializer import B_tagSerializer


# DAO
class B_tagRepository(object):
    def get_all(self):
        return Response(B_tagSerializer(B_tag.objects.all(), many=True).data)

    def find_by_id(self):
        return Response(B_tagSerializer(B_tag.objects.all(), many=True).data)