(() => {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
    })
})()


$(document).ready(function () {
    const citySelect = document.getElementById('id_city');

    fetch('/get_cities/')
        .then(response => response.json())
        .then(data => {
            citySelect.innerHTML = '';
            let option = new Option('---------', '', true, true);
            option.disabled = true;
            $('#id_city').append(option);

            let cities = Object.values(data.cities);
            cities.forEach(function (data) {
                // İl seçeneklerini oluştur
                option = new Option(data.city, data.city);
                $('#id_city').append(option);
            });
        });
});

function getCounties(select) {
    const city = select.value;
    const countySelect = document.getElementById('id_county');

    clearSelected('id_county');

    fetch(select.getAttribute('data-county-url') + '?city=' + city)
        .then(response => response.json())
        .then(data => {
            countySelect.innerHTML = '';
            let option = new Option('---------', '', true, true);
            option.disabled = true;
            $('#id_county').append(option);

            let counties = Object.values(data.counties);
            counties.forEach(function (data) {
                // İlçe seçeneklerini oluştur
                option = new Option(data.county, data.county);
                $('#id_county').append(option);
            });
        });
}

function getHospitals(select) {
    const county = select.value;
    const citySelect = document.getElementById('id_city');
    const hospitalSelect = document.getElementById('id_hospital');

    clearSelected('id_hospital')

    const city = citySelect.value;

    fetch(select.getAttribute('data-hospital-url') + '?city=' + city + '&county=' + county)
        .then(response => response.json())
        .then(data => {
            hospitalSelect.innerHTML = '';
            let option = new Option('---------', '', true, true);
            option.disabled = true;
            $('#id_hospital').append(option);

            let hospitals = Object.values(data.hospitals);
            hospitals.forEach(function (data) {
                // Hastane seçeneklerini oluştur
                option = new Option(data.hospital, data.hospital);
                $('#id_hospital').append(option);
            });
        });
}

function getClinics(select) {
    const hospital = select.value;
    const citySelect = document.getElementById('id_city');
    const countySelect = document.getElementById('id_county');
    const clinicSelect = document.getElementById('id_clinic');

    clearSelected('id_clinic');

    const city = citySelect.value;
    const county = countySelect.value;

    fetch(select.getAttribute('data-clinic-url') + '?city=' + city + '&county=' + county + '&hospital=' + hospital)
        .then(response => response.json())
        .then(data => {
            clinicSelect.innerHTML = '';
            let option = new Option('---------', '', true, true);
            option.disabled = true;
            $('#id_clinic').append(option);

            let clinics = Object.values(data.clinics);
            clinics.forEach(function (data) {
                // Hastane seçeneklerini oluştur
                option = new Option(data.clinic, data.clinic);
                $('#id_clinic').append(option);
            });
        });
}

function getDoctors(select) {
    const clinic = select.value;
    const citySelect = document.getElementById('id_city');
    const countySelect = document.getElementById('id_county');
    const hospitalSelect = document.getElementById('id_hospital');
    const doctorSelect = document.getElementById('id_doctor');

    clearSelected('id_doctor');

    const city = citySelect.value;
    const county = countySelect.value;
    const hospital = hospitalSelect.value;

    fetch(select.getAttribute('data-doctor-url') + '?city=' + city + '&county=' + county + '&hospital=' + hospital + '&clinic=' + clinic)
        .then(response => response.json())
        .then(data => {
            doctorSelect.innerHTML = '';
            let option = new Option('---------', '', true, true);
            option.disabled = true;
            $('#id_doctor').append(option);

            let doctors = Object.values(data.doctors);
            doctors.forEach(function (data) {
                // Doktor seçeneklerini oluştur
                option = new Option(data.name, data.id);
                $('#id_doctor').append(option);
            });
        });
}

function getDates(select) {
    const doctor = select.value;
    const citySelect = document.getElementById('id_city');
    const countySelect = document.getElementById('id_county');
    const hospitalSelect = document.getElementById('id_hospital');
    const clinicSelect = document.getElementById('id_clinic');
    const dateSelect = document.getElementById('id_date');

    const city = citySelect.value;
    const county = countySelect.value;
    const hospital = hospitalSelect.value;
    const clinic = clinicSelect.value;

    fetch(select.getAttribute('data-date-url') + '?city=' + city + '&county=' + county + '&hospital=' + hospital + '&clinic=' + clinic + '&doctor=' + doctor)
        .then(response => response.json())
        .then(data => {
            dateSelect.innerHTML = '';
            let dates = Object.values(data.dates);
            let option;
            if (dates.length === 0) {
                option = new Option('Randevu bulunamadı', 'Randevu bulunamadı', true, true);
            } else {
                option = new Option('---------', '', true, true);
            }
            option.disabled = true;
            $('#id_date').append(option);

            dates.forEach(function (data) {
                // Tarih seçeneklerini oluştur
                option = new Option(data.date, data.date);
                $('#id_date').append(option);
            });
        });
}

function clearSelected(select) {
    const hospitalSelect = document.getElementById('id_hospital');
    const clinicSelect = document.getElementById('id_clinic');
    const doctorSelect = document.getElementById('id_doctor');
    const dateSelect = document.getElementById('id_date');

    if (select === 'id_county') {
        hospitalSelect.innerHTML = '';
        clinicSelect.innerHTML = '';
        doctorSelect.innerHTML = '';
        dateSelect.innerHTML = '';
    } else if (select === 'id_hospital') {
        clinicSelect.innerHTML = '';
        doctorSelect.innerHTML = '';
        dateSelect.innerHTML = '';
    } else if (select === 'id_clinic') {
        doctorSelect.innerHTML = '';
        dateSelect.innerHTML = '';
    } else if (select === 'id_doctor') {
        dateSelect.innerHTML = '';
    }
}
