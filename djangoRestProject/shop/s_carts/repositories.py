
from django.http import JsonResponse
from rest_framework.response import Response

from shop.s_carts.models import S_cart
from shop.s_carts.serializer import S_cartSerializer


# DAO
class S_cartRepository(object):
    def get_all(self):
        return Response(S_cartSerializer(S_cart.objects.all(), many=True).data)

    def find_by_id(self):
        return Response(S_cartSerializer(S_cart.objects.all(), many=True).data)
