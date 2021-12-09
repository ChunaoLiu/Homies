from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        id = serializers.IntegerField(source='pk')
        fields = ['pk', 'email', 'password']