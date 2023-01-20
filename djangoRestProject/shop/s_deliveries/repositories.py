
from django.http import JsonResponse
from rest_framework.response import Response

from shop.s_deliveries.models import S_delivery
from shop.s_deliveries.serializer import S_deliverySerializer





# DAO
class S_deliveryRepository(object):
    def get_all(self):
        return Response(S_deliverySerializer(S_delivery.objects.all(), many=True).data)

    def find_by_id(self):
        return Response(S_deliverySerializer(S_delivery.objects.all(), many=True).data)

