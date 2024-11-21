from rest_framework import serializers
from .models import PrescriptionApp

class PrescriptionAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionApp
        fields = '__all__'