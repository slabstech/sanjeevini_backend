from rest_framework import serializers
from .models import DoctorAppointmentApp

class DoctorAppointmentAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAppointmentApp
        fields = '__all__'