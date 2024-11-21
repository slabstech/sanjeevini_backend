from rest_framework import serializers
from .models import DoctorApp

class DoctorAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorApp
        fields = '__all__'