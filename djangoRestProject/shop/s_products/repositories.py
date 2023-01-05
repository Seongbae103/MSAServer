
from django.http import JsonResponse
from rest_framework.response import Response

from shop.s_products.models import S_product
from shop.s_products.serializer import S_productSerializer


# DAO
class S_productRepository(object):
    def get_all(self):
        return Response(S_productSerializer(S_product.objects.all(), many=True).data)

    def find_by_id(self):
        return Response(S_productSerializer(S_product.objects.all(), many=True).data)

