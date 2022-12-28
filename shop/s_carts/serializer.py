from rest_framework import serializers
from models import S_cart

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = S_cart
        fields = '__all__'