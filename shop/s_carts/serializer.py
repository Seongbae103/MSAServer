from rest_framework import serializers
from rest_framework.response import Response

from shop.s_carts.models import S_cart


class S_cartSerializer(serializers.ModelSerializer):
    class Meta:
        model = S_cart
        fields = '__all__'

    def create(self, validated_data):
        return S_cart.objects.create(**validated_data)

    def update(self, instance, valicated_data):
        S_cart.objects.filter(pk=instance.id).update(**valicated_data)

    def get_all(self):
        return Response(S_cartSerializer(S_cart.objects.all(), many=True).data)

    def delete(self):
        pass

    def find_by_cart_id(self):  # get은 그냥 가져오는 것이고 조건에 맞는 것을 가져오는건 find니까 ~by에서는 find를 사용
        pass

    def delete(self):
        pass