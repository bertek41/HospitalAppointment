from datetime import datetime, timedelta

from django.conf import settings

from django.contrib import admin

from HospitalAppointment.forms import AppointmentDateForm


class AppointmentDateAdmin(admin.ModelAdmin):
    list_display = ("doctor", "date", "get_clinic", "get_hospital")
    search_fields = ("doctor__name", "date", "doctor__clinic", "doctor__hospital")
    list_filter = ("doctor", "date", "doctor__clinic", "doctor__hospital")
    exclude = ("date",)
    form = AppointmentDateForm
    change_form_template = "admin/appointment_date_change_form.html"

    def get_clinic(self, obj):
        return obj.doctor.clinic

    def get_hospital(self, obj):
        return obj.doctor.hospital

    get_clinic.admin_order_field = "doctor__clinic"
    get_clinic.short_description = "Klinik"
    get_hospital.admin_order_field = "doctor__hospital"
    get_hospital.short_description = "Hastane"

    def save_model(self, request, obj, form, change):
        # Get data from form
        start_date = form.cleaned_data["start_date"]
        end_date = form.cleaned_data["end_date"]
        include_weekends = form.cleaned_data["include_weekends"]
        start_time = form.cleaned_data["start_time"]
        start_time = start_time.replace(second=0, microsecond=0)
        end_time = form.cleaned_data["end_time"]
        end_time = end_time.replace(second=0, microsecond=0)
        appointment_duration = form.cleaned_data["appointment_duration"]
        appointment_delay = form.cleaned_data["appointment_delay"]
        lunch_start_time = form.cleaned_data["lunch_start_time"]
        lunch_start_time = lunch_start_time.replace(second=0, microsecond=0)
        lunch_end_time = form.cleaned_data["lunch_end_time"]
        lunch_end_time = lunch_end_time.replace(second=0, microsecond=0)

        end_datetime = datetime.combine(end_date, end_time)

        # Calculate the idle time
        time_delta = timedelta(minutes=appointment_duration + appointment_delay)

        # Make sure that the end datetime is not included in the appointment time
        end_datetime -= timedelta(minutes=appointment_duration)

        current_datetime = datetime.combine(start_date, start_time)
        current_end_datetime = (
            datetime.combine(start_date, end_time)
            if start_time < end_time
            else datetime.combine(start_date + timedelta(days=1), end_time)
        )
        appointment_datetimes = []

        while current_datetime <= end_datetime:
            # Weekends check
            if not include_weekends:
                if current_datetime.weekday() == 5:
                    current_datetime = datetime.combine(
                        current_datetime.date() + timedelta(days=2), start_time
                    )
                    current_end_datetime = datetime.combine(
                        current_datetime.date(), end_time
                    )
                    continue
                elif current_datetime.weekday() == 6:
                    current_datetime = datetime.combine(
                        current_datetime.date() + timedelta(days=1), start_time
                    )
                    current_end_datetime = datetime.combine(
                        current_datetime.date(), end_time
                    )
                    continue
            # End time check
            if current_datetime >= current_end_datetime:
                current_datetime = datetime.combine(
                    current_datetime.date() + timedelta(days=1), start_time
                )
                current_end_datetime = datetime.combine(
                    current_datetime.date(), end_time
                )
                continue

            # Lunch check
            if lunch_start_time <= current_datetime.time() < lunch_end_time:
                current_datetime += time_delta
                continue
            elif current_datetime.time() >= lunch_end_time:
                appointment_datetimes.append(current_datetime)
                current_datetime += time_delta
            else:
                appointment_datetimes.append(current_datetime)
                current_datetime += time_delta - timedelta(minutes=appointment_delay)

        if not appointment_datetimes:
            print("No appointments created")
        else:
            obj.date = appointment_datetimes[-1]

            # Save dates
            for appointment_datetime in appointment_datetimes[:-1]:
                obj.doctor.dates.create(date=appointment_datetime)

            super().save_model(request, obj, form, change)

    def add_view(self, request, form_url="", extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context["TR_CONDITIONS"] = settings.TR_CONDITIONS
        return super(AppointmentDateAdmin, self).add_view(
            request, form_url, extra_context
        )

    def change_view(self, request, object_id, form_url="", extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context["TR_CONDITIONS"] = settings.TR_CONDITIONS
        return super(AppointmentDateAdmin, self).change_view(
            request, object_id, extra_context=extra_context
        )


def add_minutes(tm, minutes):
    fulldate = datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + timedelta(minutes=minutes)
    return fulldate.time()
