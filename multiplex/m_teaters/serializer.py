from rest_framework import serializers
from models import M_theater

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = M_theater
        fields = '__all__'