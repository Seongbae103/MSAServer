from rest_framework import serializers
from rest_framework.response import Response

from shop.s_orders.models import S_order


class S_orderSerializer(serializers.ModelSerializer):
    class Meta:
        model = S_order
        fields = '__all__'

    def create(self, validated_data):
        return S_order.objects.create(**validated_data)

    def update(self, instance, valicated_data):
        S_order.objects.filter(pk=instance.id).update(**valicated_data)

    def get_all(self):
        return Response(S_orderSerializer(S_order.objects.all(), many=True).data)

    def delete(self):
        pass

    def find_order_by_id(self):  # get은 그냥 가져오는 것이고 조건에 맞는 것을 가져오는건 find니까 ~by에서는 find를 사용
        pass

    def delete(self):
        pass