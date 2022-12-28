from rest_framework import serializers
from models import B_post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = B_post
        fields = '__all__'