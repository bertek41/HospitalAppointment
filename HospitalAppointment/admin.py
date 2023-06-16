from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .admins.appointment_admin import AppointmentAdmin
from .admins.appointment_date_admin import AppointmentDateAdmin
from .models import User, Doctor, AppointmentDate, Appointment, Blog
from HospitalAppointment.admins import DoctorAdmin, BlogAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(AppointmentDate, AppointmentDateAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Blog, BlogAdmin)
