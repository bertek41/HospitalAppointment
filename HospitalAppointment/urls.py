"""
URL configuration for HospitalAppointment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic import RedirectView

from HospitalAppointment import views

urlpatterns = (
    [
        path(
            "admin/",
            admin.site.urls,
        ),
        path("", views.index, name="index"),
        path("signup/", views.signup, name="signup"),
        path("login/", views.account_login, name="account_login"),
        path("logout/", views.account_logout, name="account_logout"),
        path("appointment/get/", views.get_appointment, name="get_appointment"),
        path("appointment/", views.list_appointment, name="list_appointment"),
        path(
            "appointment/cancel/<int:appointment_id>",
            views.cancel_appointment,
            name="appointment_cancel",
        ),
        path("get_cities/", views.get_cities, name="get_cities"),
        path("get_counties/", views.get_counties, name="get_counties"),
        path("get_hospitals/", views.get_hospitals, name="get_hospitals"),
        path("get_clinics/", views.get_clinics, name="get_clinics"),
        path("get_doctors/", views.get_doctors, name="get_doctors"),
        path("get_dates/", views.get_dates, name="get_dates"),
        path(
            "favicon.ico",
            RedirectView.as_view(url=staticfiles_storage.url("icons/favicon.ico")),
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
