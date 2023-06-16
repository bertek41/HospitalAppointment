from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(
                "^\\s*?[0-9]{1,11}\\s*$",
                "Lütfen geçerli bir TC kimlik numarası giriniz.",
            )
        ],
        help_text="TC Kimlik numaranızı giriniz.",
        error_messages={
            "unique": "Bu TC Kimliğe ait bir hesap zaten bulunmakta.",
            "invalid": "Lütfen geçerli bir TC kimlik numarası giriniz.",
        },
        verbose_name="TC Kimlik Numarası",
    )
    birthdate = models.DateField(null=True, blank=True, verbose_name="Doğum Tarihi")


class Doctor(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="İsim")
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name="Şehir")
    county = models.CharField(max_length=50, null=True, blank=True, verbose_name="İlçe")
    clinic = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Klinik"
    )
    hospital = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Hastane"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Doktor"
        verbose_name_plural = "Doktorlar"


class Appointment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Kullanıcı",
        related_name="appointments",
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        verbose_name="Doktor",
        related_name="appointments",
    )
    date = models.DateTimeField(verbose_name="Tarih ve Saat")

    class Meta:
        verbose_name = "Randevu"
        verbose_name_plural = "Randevular"


class AppointmentDate(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, verbose_name="Doktor", related_name="dates"
    )
    date = models.DateTimeField(verbose_name="Tarih ve Saat")

    class Meta:
        verbose_name = "Randevu Tarihi"
        verbose_name_plural = "Randevu Tarihleri"


class Blog(models.Model):
    title = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Başlık"
    )
    content = models.TextField(null=True, blank=True, verbose_name="İçerik")
    date = models.DateTimeField(verbose_name="Tarih")

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Bloglar"
