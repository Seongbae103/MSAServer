
from django.http import JsonResponse
from rest_framework.response import Response

from shop.s_categories.models import S_category
from shop.s_categories.serializer import S_categorySerializer


# DAO
class S_categoryRepository(object):
    def get_all(self):
        return Response(S_categorySerializer(S_category.objects.all(), many=True).data)

    def find_by_id(self):
        return Response(S_categorySerializer(S_category.objects.all(), many=True).data)
