from rest_framework import serializers
from .models import UserMaternityApp

class UserMaternityAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMaternityApp
        fields = '__all__'