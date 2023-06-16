# Generated by Django 4.2 on 2023-05-02 19:29

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("HospitalAppointment", "0005_remove_user_id_number_alter_user_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="dates",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.DateTimeField(), blank=True, null=True, size=None
            ),
        ),
        migrations.CreateModel(
            name="Appointment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField(verbose_name="Tarih ve Saat")),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="HospitalAppointment.doctor",
                        verbose_name="Doktor",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Kullanıcı",
                    ),
                ),
            ],
            options={
                "verbose_name": "Randevu",
                "verbose_name_plural": "Randevular",
            },
        ),
    ]
