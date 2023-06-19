from django.contrib import admin


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("user", "doctor", "date", "get_clinic", "get_hospital")
    search_fields = (
        "user__username",
        "user__first_name",
        "doctor__name",
        "date",
        "doctor__clinic",
        "doctor__hospital",
    )
    list_filter = ("user", "doctor", "date", "doctor__clinic", "doctor__hospital")

    def get_clinic(self, obj):
        return obj.doctor.clinic

    def get_hospital(self, obj):
        return obj.doctor.hospital

    get_clinic.admin_order_field = "doctor__clinic"
    get_clinic.short_description = "Klinik"
    get_hospital.admin_order_field = "doctor__hospital"
    get_hospital.short_description = "Hastane"

    class Meta:
        model = "HospitalAppointment.Appointment"
