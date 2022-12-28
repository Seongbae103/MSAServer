from rest_framework import serializers
from models import B_comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = B_comment
        fields = '__all__'