# Generated by Django 5.1.1 on 2024-11-22 00:16

from django.db import migrations

def add_default_entries(apps, schema_editor):
    UserWeightApp = apps.get_model('userweightapp', 'UserWeightApp')
    UserWeightApp.objects.create(appointment_day='2024-11-19', weight=70.5, appointment_time='10:00:00', patient_name='Dr. Kini', status='Pending', observations='Follow-up appointment')
    UserWeightApp.objects.create(appointment_day='2024-11-21', weight=68.3, appointment_time='14:30:00', patient_name='Dr. Chandan Kamath', status='Confirmed', observations='Routine check-up')
    UserWeightApp.objects.create(appointment_day='2024-12-04', weight=75.0, appointment_time='09:00:00', patient_name='Dr. Prashan Kumar', status='Cancelled', observations='Patient unavailable')


class Migration(migrations.Migration):

    dependencies = [
        ('userweightapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_entries),
    ]