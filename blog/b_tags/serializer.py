from rest_framework import serializers
from models import B_tag

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = B_tag
        fields = '__all__'