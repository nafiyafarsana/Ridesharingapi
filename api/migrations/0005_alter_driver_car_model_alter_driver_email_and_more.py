# Generated by Django 5.0.4 on 2024-05-01 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_driver_car_model_driver_email_driver_license_plate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='car_model',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='driver',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='driver',
            name='license_plate',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='driver',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
    ]
