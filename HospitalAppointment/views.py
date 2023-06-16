from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from HospitalAppointment.forms import (
    SignupForm,
    LoginForm,
    GetAppointmentForm,
)
from HospitalAppointment.models import Doctor, AppointmentDate, Appointment, Blog
from HospitalAppointment.utils import id_check


def index(request):
    blogs = Blog.objects.all().order_by("-date")[:6]
    doctors = Doctor.objects.all()[0:6]
    return render(request, "index.html", {"blogs": blogs, "doctors": doctors})


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            year = form.cleaned_data.get("birthdate").year
            if not id_check.check_civil(
                username,
                first_name,
                last_name,
                year,
            ):
                return render(
                    request,
                    "signup.html",
                    {
                        "form": form,
                        "error": "TC Kimlik Numarası, Ad, Soyad ve Doğum Yılı bilgileri uyuşmuyor.",
                    },
                )
            form.save()
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect("index")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})


def account_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                return render(
                    request,
                    "login.html",
                    {"form": form, "error": "Kullanıcı adı veya şifre yanlış."},
                )
        else:
            return render(
                request,
                "login.html",
                {"form": form, "error": "Kullanıcı adı veya şifre yanlış."},
            )
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def account_logout(request):
    logout(request)
    return redirect("index")


def get_cities(request):
    cities = []

    try:
        cities = Doctor.objects.values("city")
    except Doctor.DoesNotExist:
        pass

    data = {"cities": list(cities)}
    return JsonResponse(data)


def get_counties(request):
    city_id = request.GET.get("city")
    counties = []

    if city_id:
        try:
            counties = Doctor.objects.filter(city=city_id).values("county")
        except Doctor.DoesNotExist:
            pass

    data = {"counties": list(counties)}
    return JsonResponse(data)


def get_hospitals(request):
    city_id = request.GET.get("city")
    county_id = request.GET.get("county")
    hospitals = []

    if city_id and county_id:
        try:
            doctor_ids = Doctor.objects.filter(
                city=city_id, county=county_id
            ).values_list("id", flat=True)
            hospitals = Doctor.objects.filter(id__in=doctor_ids).values("hospital")
        except Doctor.DoesNotExist:
            pass

    data = {"hospitals": list(hospitals)}
    return JsonResponse(data)


def get_clinics(request):
    city_id = request.GET.get("city")
    county_id = request.GET.get("county")
    hospital_id = request.GET.get("hospital")
    clinics = []

    if city_id and county_id and hospital_id:
        try:
            doctor_ids = Doctor.objects.filter(
                city=city_id, county=county_id, hospital=hospital_id
            ).values_list("id", flat=True)
            clinics = Doctor.objects.filter(id__in=doctor_ids).values("clinic")
        except Doctor.DoesNotExist:
            pass

    data = {"clinics": list(clinics)}
    return JsonResponse(data)


def get_doctors(request):
    city_id = request.GET.get("city")
    county_id = request.GET.get("county")
    hospital_id = request.GET.get("hospital")
    clinic_id = request.GET.get("clinic")
    doctors = []

    if city_id and county_id and hospital_id and clinic_id:
        try:
            doctors = Doctor.objects.filter(
                city=city_id, county=county_id, hospital=hospital_id, clinic=clinic_id
            )
        except Doctor.DoesNotExist:
            pass

    data = {"doctors": list(doctors.values("name", "id"))}
    return JsonResponse(data)


def get_dates(request):
    doctor_id = request.GET.get("doctor")
    dates = []

    if doctor_id:
        try:
            dates = (
                AppointmentDate.objects.filter(doctor=doctor_id).filter(
                    date__gte=timezone.now()
                )
            ).values("date")
        except Doctor.DoesNotExist:
            pass

    for date in dates:
        date["date"] = date["date"].strftime("%d.%m.%Y %H:%M")

    dates = sorted(dates, key=lambda k: k["date"])

    data = {"dates": list(dates)}
    return JsonResponse(data)


@login_required(login_url="/login/")
def get_appointment(request):
    form = GetAppointmentForm(current_user=request.user)

    if request.method == "POST":
        form = GetAppointmentForm(request.POST, current_user=request.user)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()

            appointment_date = form.cleaned_data.get("date")
            doctor = form.cleaned_data.get("doctor")
            appointment_date = AppointmentDate.objects.filter(
                date=appointment_date, doctor=doctor
            ).first()
            appointment_date.delete()

            return render(
                request,
                "get_appointment.html",
                {"form": form, "appointment": appointment},
            )

    return render(request, "get_appointment.html", {"form": form})


@login_required(login_url="/login/")
def list_appointment(request):
    user = request.user
    appointments = Appointment.objects.filter(user=user)

    context = {
        "appointments": appointments,
    }
    return render(request, "appointment.html", context)


@login_required(login_url="/login/")
def cancel_appointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return redirect("list_appointment")

    appointment.delete()

    if appointment.date >= timezone.now():
        appointment_date = AppointmentDate.objects.create(
            doctor=appointment.doctor, date=appointment.date
        )
        appointment_date.save()

    return redirect("list_appointment")
