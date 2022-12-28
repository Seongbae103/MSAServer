from rest_framework import serializers
from models import M_theaterTicket

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = M_theaterTicket
        fields = '__all__'