from django.contrib import admin


class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "county", "clinic", "hospital")
    search_fields = ("name", "city", "county", "clinic", "hospital")
    list_filter = ("city", "county", "clinic", "hospital")
