from django.db import models

class UserDiabetesApp(models.Model):
    id = models.BigAutoField(primary_key=True)
    patient_name = models.CharField(max_length=255)
    blood_glucose_level = models.DecimalField(max_digits=5, decimal_places=2)
    measurement_date = models.DateField()
    measurement_time = models.TimeField()
    meal_type = models.CharField(max_length=255)
    medication_dose = models.DecimalField(max_digits=5, decimal_places=2)
    medication_name = models.CharField(max_length=255)
    medication_time = models.TimeField()
    physical_activity = models.CharField(max_length=255)
    duration = models.IntegerField()
    notes = models.TextField()