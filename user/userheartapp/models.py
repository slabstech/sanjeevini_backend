from django.db import models

class UserHeartApp(models.Model):
    id = models.BigAutoField(primary_key=True)
    appointment_day = models.DateField()
    appointment_time = models.TimeField()
    patient_name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    observations = models.TextField()

    # Heart vital signs
    heart_rate = models.IntegerField()                 # Heart rate in beats per minute
    blood_pressure_systolic = models.IntegerField()     # Systolic blood pressure in mmHg
    blood_pressure_diastolic = models.IntegerField()    # Diastolic blood pressure in mmHg
    oxygen_saturation = models.DecimalField(max_digits=4, decimal_places=2) # Oxygen saturation in percentage