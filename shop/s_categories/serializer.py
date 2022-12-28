from rest_framework import serializers
from models import S_category

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = S_category
        fields = '__all__'