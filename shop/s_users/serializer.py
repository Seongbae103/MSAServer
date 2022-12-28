from rest_framework import serializers
from models import S_user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = S_user
        fields = '__all__'