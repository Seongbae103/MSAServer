from rest_framework import serializers
from models import M_cinema

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = M_cinema
        fields = '__all__'