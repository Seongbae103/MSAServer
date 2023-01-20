from rest_framework import serializers
from rest_framework.response import Response

from blog.b_posts.models import B_post


class B_postSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField()
    password = serializers.CharField()
    user_name = serializers.CharField()
    phone = serializers.CharField()
    birth = serializers.CharField()
    address = serializers.CharField()
    job = serializers.CharField()
    user_interests = serializers.CharField()
    token = serializers.CharField()

    class Meta:
        model = B_post
        fields = '__all__'

    def create(self, validated_data):
        return B_post.objects.create(**validated_data)

    def update(self, instance, valicated_data):
        B_post.objects.filter(pk=instance.id).update(**valicated_data)

    def get_all(self):
        return Response(B_postSerializer(B_post.objects.all(), many=True).data)

    def delete(self):
        pass

    def find_post_by_id(self):  # get은 그냥 가져오는 것이고 조건에 맞는 것을 가져오는건 find니까 ~by에서는 find를 사용
        pass

    def delete(self):
        pass