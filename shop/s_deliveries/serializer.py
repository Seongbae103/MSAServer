from rest_framework import serializers
from models import S_delivery

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = S_delivery
        fields = '__all__'