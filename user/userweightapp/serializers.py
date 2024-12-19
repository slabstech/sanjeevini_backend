from rest_framework import serializers
from .models import UserWeightApp

class UserWeightAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWeightApp
        fields = '__all__'