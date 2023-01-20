
from django.http import JsonResponse
from rest_framework.response import Response

from shop.s_orders.models import S_order
from shop.s_orders.serializer import S_orderSerializer



# DAO
class S_orderRepository(object):
    def get_all(self):
        return Response(S_orderSerializer(S_order.objects.all(), many=True).data)

    def find_by_id(self):
        return Response(S_orderSerializer(S_order.objects.all(), many=True).data)
