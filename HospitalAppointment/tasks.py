from celery import shared_task
from django.utils import timezone

from HospitalAppointment.models import Appointment, AppointmentDate


@shared_task(soft_time_limit=60, time_limit=120)
def remove_expired_appointments():
    Appointment.objects.filter(date__lt=timezone.now()).delete()


@shared_task(soft_time_limit=60, time_limit=120)
def remove_expired_appointment_dates():
    AppointmentDate.objects.filter(date__lt=timezone.now()).delete()
