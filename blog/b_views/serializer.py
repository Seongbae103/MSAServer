from rest_framework import serializers
from models import B_view

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = B_view
        fields = '__all__'