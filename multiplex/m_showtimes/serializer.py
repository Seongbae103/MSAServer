from rest_framework import serializers
from models import M_showtime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = M_showtime
        fields = '__all__'