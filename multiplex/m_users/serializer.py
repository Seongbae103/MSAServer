from rest_framework import serializers
from models import M_user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = M_user
        fields = '__all__'