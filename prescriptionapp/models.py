from django.db import models
class PrescriptionApp(models.Model):
    id = models.BigAutoField(primary_key=True)
    issue_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    doctor_full_name = models.CharField(max_length=255)
    medication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    frequency = models.CharField(max_length=255)
    refill_info = models.CharField(max_length=255, blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)