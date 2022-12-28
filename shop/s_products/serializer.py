from rest_framework import serializers
from models import S_product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = S_product
        fields = '__all__'