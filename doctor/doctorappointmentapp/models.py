from django.db import models

class DoctorAppointmentApp(models.Model):
    id = models.BigAutoField(primary_key=True)
    appointment_day = models.DateField()
    appointment_time = models.TimeField()
    patient_name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    observations = models.TextField()