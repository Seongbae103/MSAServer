from rest_framework import serializers
from models import B_user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = B_user
        fields = '__all__'