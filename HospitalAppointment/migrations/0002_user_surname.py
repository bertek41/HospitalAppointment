# Generated by Django 4.2 on 2023-04-24 17:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("HospitalAppointment", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="surname",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
