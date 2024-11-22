# Generated by Django 5.1.1 on 2024-11-21 21:42

from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserHeartApp',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('appointment_day', models.DateField()),
                ('appointment_time', models.TimeField()),
                ('patient_name', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('observations', models.TextField()),
                ('heart_rate', models.IntegerField()),
                ('blood_pressure_systolic', models.IntegerField()),
                ('blood_pressure_diastolic', models.IntegerField()),
                ('oxygen_saturation', models.DecimalField(max_digits=4, decimal_places=2)),
            ],
        ),
    ]