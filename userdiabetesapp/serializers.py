from rest_framework import serializers
from .models import UserDiabetesApp

class UserDiabetesAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDiabetesApp
        fields = '__all__'