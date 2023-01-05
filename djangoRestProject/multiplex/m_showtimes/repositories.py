from django.http import JsonResponse
from rest_framework.response import Response

from multiplex.m_showtimes.models import M_showtime
from multiplex.m_showtimes.serializer import M_showtimeSerializer


# DAO
class M_showtimeRepository(object):
    def get_all(self):
        return Response(M_showtimeSerializer(M_showtime.objects.all(), many=True).data)

    def find_by_id(self):
        return Response(M_showtimeSerializer(M_showtime.objects.all(), many=True).data)

    def login(self, kwargs):
        loginUser = M_showtime.objects.get(user_email=kwargs["user_email"])
        print(f"해당 email 을 가진  User ID: *** \n {loginUser.id}")
        if loginUser.password == kwargs["password"]:
            dbUser = M_showtime.objects.all().filter(id=loginUser.id).values()[0]
            print(f" DBUser is {dbUser}")
            serializer = M_showtimeSerializer(loginUser, many=False)
            return JsonResponse(data=serializer.data,
                                safe=False)  # == return JsonResponse({"data":serializer.data, "safe":False})
        else:
            return JsonResponse({"data" : "WRONG_PASSWORD"}) #JsonResponse가 리액트로 보내주는 DTO

