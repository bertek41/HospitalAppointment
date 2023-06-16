from django.contrib import admin


class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "date")
    search_fields = ("title", "content", "date")
    list_filter = ("title", "content", "date")

    class Meta:
        model = "HospitalAppointment.Blog"
