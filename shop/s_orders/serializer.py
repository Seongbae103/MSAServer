
from rest_framework import serializers
from models import S_order

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = S_order
        fields = '__all__'