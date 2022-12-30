from django.http import JsonResponse
from rest_framework.response import Response
from security.users.models import User
from security.users.serializer import UserSerializer


# DAO
class UserRepository(object):
    def get_all(self):
        return Response(UserSerializer(User.objects.all(), many=True).data)

    def find_by_id(self, id):
        return User.objects.all().filter(id=id).values()[0]

    def login(self, param):
        print(f"유저 이메일 : {param['user_email']}")
        loginUser = User.objects.get(user_email=param['user_email'])
        print(f"해당 email 을 가진  User ID: *** \n {loginUser.id}")
        if loginUser.password == param["password"]:
            dbUser = self.find_by_id(loginUser.id)
            print(f" DBUser is {dbUser}")
            serializer = UserSerializer(loginUser, many=False)
            print(serializer)
            return JsonResponse(data=serializer.data,
                                safe=False)  # == return Response({"data":serializer.data, "safe":False})
        else:
            return JsonResponse({"data" : "WRONG_PASSWORD"}) #JsonResponse가 리액트로 보내주는 DTO

    def find_user_by_email(self, param):
        return User.objects.all().filter(user_email=param).values()[0]

    def find_users_by_name(self, param):
        return User.objects.all().filter(user_name=param).values()
