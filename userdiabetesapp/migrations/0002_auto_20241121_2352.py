from django.db import migrations
from datetime import date, time

def create_dummy_entries(apps, schema_editor):
    UserDiabetesApp = apps.get_model('userdiabetesapp', 'UserDiabetesApp')

    UserDiabetesApp.objects.create(
        patient_name='John Doe',
        blood_glucose_level=105.5,
        measurement_date=date(2022, 1, 1),
        measurement_time=time(9, 0),
        meal_type='Breakfast',
        medication_dose=10,
        medication_name='Insulin',
        medication_time=time(8, 0),
        physical_activity='Walk',
        duration=30,
        notes='Felt a bit tired after breakfast.'
    )

    UserDiabetesApp.objects.create(
        patient_name='Jane Smith',
        blood_glucose_level=95.2,
        measurement_date=date(2022, 1, 2),
        measurement_time=time(9, 0),
        meal_type='Lunch',
        medication_dose=20,
        medication_name='Insulin',
        medication_time=time(12, 30),
        physical_activity='Run',
        duration=45,
        notes='Feeling better after lunch.'
    )

    UserDiabetesApp.objects.create(
        patient_name='Robert Johnson',
        blood_glucose_level=120.3,
        measurement_date=date(2022, 1, 3),
        measurement_time=time(9, 0),
        meal_type='Dinner',
        medication_dose=15,
        medication_name='Insulin',
        medication_time=time(19, 0),
        physical_activity='Swim',
        duration=60,
        notes='Felt energized after dinner.'
    )

    UserDiabetesApp.objects.create(
        patient_name='Emily Davis',
        blood_glucose_level=88.9,
        measurement_date=date(2022, 1, 4),
        measurement_time=time(9, 0),
        meal_type='Breakfast',
        medication_dose=12,
        medication_name='Insulin',
        medication_time=time(8, 0),
        physical_activity='Bike',
        duration=40,
        notes='Feeling good after breakfast.'
    )

    UserDiabetesApp.objects.create(
        patient_name='Michael Wilson',
        blood_glucose_level=110.7,
        measurement_date=date(2022, 1, 5),
        measurement_time=time(9, 0),
        meal_type='Lunch',
        medication_dose=25,
        medication_name='Insulin',
        medication_time=time(12, 30),
        physical_activity='Hike',
        duration=90,
        notes='Felt a bit tired after lunch.'
    )


    # Add more entries here...

class Migration(migrations.Migration):

    dependencies = [
        ('userdiabetesapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_dummy_entries),
    ]