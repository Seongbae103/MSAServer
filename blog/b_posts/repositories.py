from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import JsonResponse
from rest_framework.response import Response

from blog.b_posts.models import B_post
from blog.b_posts.serializer import B_postSerializer


# DAO
class B_postRepository(object):
    def get_all(self):
        return Response(B_postSerializer(B_post.objects.all(), many=True).data)

    def find_by_id(self):
        return Response(B_postSerializer(B_post.objects.all(), many=True).data)

