# Generated by Django 5.1.1 on 2024-11-19 09:22

from django.db import migrations

def add_default_entries(apps, schema_editor):
    DoctorApp = apps.get_model('doctorapp', 'DoctorApp')
    DoctorApp.objects.create(appointment_day='2024-11-19', appointment_time='10:00:00', patient_name='User 001', status='Pending', observations='Follow-up appointment')
    DoctorApp.objects.create(appointment_day='2024-11-21', appointment_time='14:30:00', patient_name='User 002', status='Confirmed', observations='Routine check-up')
    DoctorApp.objects.create(appointment_day='2024-12-04', appointment_time='09:00:00', patient_name='User 003', status='Cancelled', observations='Patient unavailable')

class Migration(migrations.Migration):

    dependencies = [
        ('doctorapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_entries),
    ]