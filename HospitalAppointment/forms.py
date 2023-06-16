import datetime

from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput
from django import forms
from django.conf import settings

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy

from HospitalAppointment.models import User, AppointmentDate, Appointment, Doctor
from HospitalAppointment.widgets import DynamicChoiceField


class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Ad",
        widget=forms.TextInput(attrs={"class": "form-control", "autofocus": True}),
        error_messages={
            "invalid": "Lütfen geçerli bir isim girin.",
            "required": "Bu alanı doldurun.",
            "blank": "Bu alanı doldurunn.",
        },
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Soyad",
        error_messages={"invalid": "Lütfen geçerli bir isim girin."},
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        label="E-posta",
        empty_value="Boş bırakma gevşek",
        error_messages={"invalid": "Lütfen geçerli bir e-posta adresi girin."},
    )
    username = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "min": 10000000000, "max": 99999999999}
        ),
        min_value=10000000000,
        max_value=99999999999,
        label="TC Kimlik No",
    )
    birthdate = forms.DateField(
        label="Doğum Tarihi",
        widget=DatePickerInput(
            options={
                "format": "DD/MM/YYYY",
                "locale": "tr",
                "allowInputToggle": True,
                "widgetPositioning": {"horizontal": "left", "vertical": "auto"},
            }
        ),
        required=True,
        localize=True,
    )

    password1 = forms.CharField(
        label="Şifre",
        widget=forms.PasswordInput(attrs={"data-toggle": "password"}),
        help_text="Şifren en az 8 karakter içermeli ve tamamen sayıdan oluşmamalı.",
    )
    password2 = forms.CharField(
        label="Şifreyi onayla",
        widget=forms.PasswordInput(attrs={"data-toggle": "password"}),
    )

    def clean_username(self):
        return str(self.cleaned_data["username"])

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "birthdate",
            "password1",
            "password2",
        )


class LoginForm(AuthenticationForm):
    username = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "min": 10000000000, "max": 99999999999}
        ),
        min_value=10000000000,
        max_value=99999999999,
        label="TC Kimlik No",
    )
    password = forms.CharField(
        label="Şifre",
        widget=forms.PasswordInput(attrs={"data-toggle": "password"}),
    )

    def clean_username(self):
        return str(self.cleaned_data["username"])

    class Meta:
        model = User
        fields = ("username", "password")


class GetAppointmentForm(forms.ModelForm):
    city = DynamicChoiceField(label="Şehir", required=True)
    county = DynamicChoiceField(label="İlçe", required=True)
    hospital = DynamicChoiceField(label="Hastane", required=True)
    clinic = DynamicChoiceField(label="Klinik", required=True)
    doctor = DynamicChoiceField(label="Doktor", required=True)
    date = DynamicChoiceField(label="Tarih ve Saat", required=True)

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)

        self.fields["city"].widget.attrs.update(
            {"class": "form-control", "id": "id_city"}
        )
        self.fields["county"].widget.attrs.update(
            {"class": "form-control", "id": "id_county"}
        )
        self.fields["hospital"].widget.attrs.update(
            {"class": "form-control", "id": "id_hospital"}
        )
        self.fields["clinic"].widget.attrs.update(
            {"class": "form-control", "id": "id_clinic"}
        )
        self.fields["doctor"].widget.attrs.update(
            {"class": "form-control", "id": "id_doctor"}
        )
        self.fields["date"].widget.attrs.update(
            {"class": "form-control", "id": "id_date"}
        )

        # Seçim yapıldığında diğer seçeneklerini güncelle
        self.fields["city"].widget.attrs.update(
            {
                "onChange": "getCounties(this);",
                "data-county-url": reverse_lazy("get_counties"),
            }
        )
        self.fields["county"].widget.attrs.update(
            {
                "onChange": "getHospitals(this);",
                "data-hospital-url": reverse_lazy("get_hospitals"),
            }
        )
        self.fields["hospital"].widget.attrs.update(
            {
                "onChange": "getClinics(this);",
                "data-clinic-url": reverse_lazy("get_clinics"),
            }
        )
        self.fields["clinic"].widget.attrs.update(
            {
                "onChange": "getDoctors(this);",
                "data-doctor-url": reverse_lazy("get_doctors"),
            }
        )
        self.fields["doctor"].widget.attrs.update(
            {
                "onChange": "getDates(this);",
                "data-date-url": reverse_lazy("get_dates"),
            }
        )

    def clean_doctor(self):
        doctor = self.cleaned_data.get("doctor")
        return Doctor.objects.get(id=doctor)

    def clean_date(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        date = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M")
        return date.strftime("%Y-%m-%d %H:%M:%S")

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get("doctor")
        date = cleaned_data.get("date")
        city = cleaned_data.get("city")
        county = cleaned_data.get("county")
        hospital = cleaned_data.get("hospital")
        clinic = cleaned_data.get("clinic")

        if doctor and date:
            if not AppointmentDate.objects.filter(doctor=doctor, date=date).exists():
                raise forms.ValidationError(
                    "Bu tarih ve saatte randevu alınamaz. Lütfen başka bir tarih seçiniz."
                )
        if city and county and hospital and clinic:
            if not Doctor.objects.filter(
                city=city, county=county, hospital=hospital, clinic=clinic
            ).exists():
                raise forms.ValidationError(
                    "Bu kriterlere uygun doktor bulunamadı. Lütfen başka bir kriter seçiniz."
                )
        if doctor and self.current_user:
            if Appointment.objects.filter(
                doctor=doctor, user=self.current_user
            ).exists():
                raise forms.ValidationError(
                    "Bu doktora zaten randevunuz bulunmaktadır."
                )

        return cleaned_data

    class Meta:
        model = Appointment
        fields = ["city", "county", "hospital", "clinic", "doctor", "date"]


class AppointmentDateForm(forms.ModelForm):
    start_date = forms.DateField(
        label="Başlangıç tarihi",
        widget=DatePickerInput(
            options={
                "format": "DD/MM/YYYY",
                "minDate": datetime.date.today(),
                "locale": "tr",
                "allowInputToggle": True,
                "showTodayButton": True,
                "showClose": True,
                "showClear": True,
                "widgetPositioning": {"horizontal": "auto", "vertical": "auto"},
            }
        ),
        required=True,
    )
    end_date = forms.DateField(
        label="Bitiş tarihi",
        widget=DatePickerInput(
            options={
                "format": "DD/MM/YYYY",
                "locale": "tr",
                "allowInputToggle": True,
                "showTodayButton": True,
                "showClose": True,
                "showClear": True,
                "widgetPositioning": {"horizontal": "auto", "vertical": "auto"},
            },
            range_from="start_date",
        ),
        required=True,
    )
    include_weekends = forms.BooleanField(
        label="Hafta sonlarını dahil et",
        widget=forms.CheckboxInput(
            attrs={
                "data-toggle": "toggle",
                "data-on": "Evet",
                "data-off": "Hayır",
                "data-onstyle": "success",
                "data-offstyle": "danger",
            }
        ),
        required=False,
    )
    start_time = forms.TimeField(
        label="Başlangıç saati",
        widget=TimePickerInput(
            options={
                "format": "HH:mm",
                "locale": "tr",
                "allowInputToggle": True,
                "showClose": True,
                "showClear": True,
                "widgetPositioning": {"horizontal": "auto", "vertical": "auto"},
            }
        ),
        required=True,
    )
    end_time = forms.TimeField(
        label="Bitiş saati",
        widget=TimePickerInput(
            options={
                "format": "HH:mm",
                "locale": "tr",
                "allowInputToggle": True,
                "showClose": True,
                "showClear": True,
                "widgetPositioning": {"horizontal": "auto", "vertical": "auto"},
            },
        ),
        required=True,
    )
    appointment_duration = forms.IntegerField(
        label="Randevu süresi",
        widget=forms.NumberInput(
            attrs={"class": "form-control w-25", "min": 1, "max": 60}
        ),
        min_value=1,
        max_value=60,
        required=True,
    )
    appointment_delay = forms.IntegerField(
        label="Randevu arası",
        widget=forms.NumberInput(
            attrs={"class": "form-control w-25", "min": 0, "max": 60}
        ),
        initial=0,
        min_value=0,
        max_value=60,
        required=True,
    )
    lunch_start_time = forms.TimeField(
        label="Öğle arası başlangıç saati",
        widget=TimePickerInput(
            options={
                "format": "HH:mm",
                "locale": "tr",
                "allowInputToggle": True,
                "showClose": True,
                "showClear": True,
                "widgetPositioning": {"horizontal": "auto", "vertical": "auto"},
            }
        ),
        required=True,
    )
    lunch_end_time = forms.TimeField(
        label="Öğle arası bitiş saati",
        widget=TimePickerInput(
            options={
                "format": "HH:mm",
                "locale": "tr",
                "allowInputToggle": True,
                "showClose": True,
                "showClear": True,
                "widgetPositioning": {"horizontal": "auto", "vertical": "auto"},
            },
        ),
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        include_weekends = cleaned_data.get("include_weekends")
        if (
            start_date.weekday() == 5 or start_date.weekday() == 6
        ) and not include_weekends:
            raise forms.ValidationError(
                "Başlangıç tarihi hafta sonuna denk geldiği için hafta sonlarını dahil et seçeneğini işaretleyin."
            )
        start_time = cleaned_data.get("start_time")
        start_time_delta = datetime.timedelta(
            hours=start_time.hour, minutes=start_time.minute
        )
        end_time = cleaned_data.get("end_time")
        end_time_delta = datetime.timedelta(
            hours=end_time.hour, minutes=end_time.minute
        )

        difference = end_time_delta - start_time_delta
        difference_as_minutes = difference.seconds / 60
        difference_as_hours = difference_as_minutes / 60

        if difference_as_minutes < cleaned_data.get(
            "appointment_duration"
        ) or difference_as_minutes < cleaned_data.get("appointment_delay"):
            raise forms.ValidationError(
                "Randevu süresi, başlangıç ve bitiş saatleri arasındaki süreden fazla olamaz."
            )
        if difference_as_hours > 12 and not settings.TR_CONDITIONS:
            raise forms.ValidationError(
                "Çalışma süresi TR şartları açılmadığı taktirde 12 saatten fazla olamaz."
            )

    class Meta:
        model = AppointmentDate
        fields = "__all__"

    class Media:
        css = {"all": ("css/appointment_date_change.css",)}
