from rest_framework import serializers
from .models import CustomUser, AudioRecord

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'access_token')

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioRecord
        fields = ('id', 'uuid', 'file')