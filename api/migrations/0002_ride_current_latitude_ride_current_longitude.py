# Generated by Django 5.0.4 on 2024-05-01 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='current_latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='current_longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]