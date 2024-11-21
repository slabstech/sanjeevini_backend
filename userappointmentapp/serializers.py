from rest_framework import serializers
from .models import UserAppointmentApp

class UserAppointmentAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAppointmentApp
        fields = '__all__'