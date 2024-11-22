from rest_framework import serializers
from .models import UserHeartApp

class UserHeartAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHeartApp
        fields = '__all__'