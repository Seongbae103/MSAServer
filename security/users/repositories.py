from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import JsonResponse
from security.users.models import User
from security.users.serializer import UserSerializer

# DAO
class UserRepository(object):
    def login(self, kwargs):
        loginUser = User.objects.get(user_email=kwargs["user_email"])
        print(f"해당 email 을 가진  User ID: *** \n {loginUser.id}")
        if loginUser.password == kwargs["password"]:
            dbUser = User.objects.all().filter(id=loginUser.id).values()[0]
            print(f" DBUser is {dbUser}")
            serializer = UserSerializer(loginUser, many=False)
            return JsonResponse(data=serializer.data,
                                safe=False)  # == return JsonResponse({"data":serializer.data, "safe":False})
        else:
            return JsonResponse({"data" : "WRONG_PASSWORD"})