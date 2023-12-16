#views.py
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import PatientSignUpForm
from .models import Doctor,Patient,Appointment,Availability, SPECIALITY_CHOICES
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, time
from .decorators import admin_forbiden


def contacts(request):
    return render(request, 'contacts.html', {})
# - User register / login

@admin_forbiden
def profil(request):
    return render(request, 'profil.html', {})

@admin_forbiden
def user_login(request):
        return render(request, 'login.html', {})

def home(request):
    if request.user.is_staff:
        return redirect('dashboard')
    else :
        return render(request, 'home.html', {})

@admin_forbiden
def login_patient(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('dashboard')
            else :
                return redirect('home')
        
        else :
            messages.error(request, "Login failed !")
            return redirect('login_patient')

    else :
        return render(request, 'login_form.html')

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out !")
    return  redirect('home')

@admin_forbiden
def register_user(request):
    if request.method == "POST":
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if get_user_model().objects.filter(email=email).exists():
                messages.error(request, "Register failed : email already used.")
                return redirect('register')

            form.save()

            user = authenticate(request, email=email, password=form.cleaned_data['password1'])
            login(request, user)

            messages.success(request, "Register successed  !")
            return redirect('home')

        else:
            messages.error(request, "Register failed !")
            return redirect('register')
    else:
        form = PatientSignUpForm()

    return render(request, 'register.html', {'form': form})

# - Booking system

@admin_forbiden
def booking(request):

    doctors = Doctor.objects.all()
    context = {
        'specialities': SPECIALITY_CHOICES,
        'doctors': doctors,
        
    }
    return render(request, 'appointment.html', context)


from django.shortcuts import render

@admin_forbiden
@login_required(login_url='home')
def get_availabilities(request):
    try:
        doctor_id = int(request.GET.get('doctor_id'))
        availabilities = Availability.objects.filter(doctor_id=doctor_id)

        availability_data = {}  # Dictionnaire pour stocker les données
        availability_list = []  # Liste pour stocker tous les objets Availability

        for availability in availabilities:
            # Ajouter l'objet Availability à la liste
            availability_list.append(availability)
            # Ajouter les heures disponibles à la liste correspondante dans le dictionnaire
            date_str = str(availability.date)
            if date_str not in availability_data:
                availability_data[date_str] = []
            availability_data[date_str].append((availability.start_time, availability.end_time))

        context = {
            'doctor_id' : doctor_id,
            'patient_id': request.user.id,
            'availability_dates': list(availability_data.keys()),
            'availabilities': availability_list,
            'availability_hours': availability_data,
        }

        return render(request, 'availabilities_accordion.html', context)
    except ValueError:
        return HttpResponseBadRequest('Invalid doctor_id parameter. It should be an integer.')

def convert_time_string(time_str):
    try:
        num_time,meridiem = time_str.split(" ")
        # Diviser la chaîne en composants
        if ":" in num_time:
            hours, minutes = num_time.split(":")
        else:
            hours = num_time
            minutes = "00"

        # Convertir les heures en entier
        hours = int(hours)
        minutes = int(minutes)

        # Ajuster l'heure pour le format PM
        if meridiem.lower() == "p.m" and hours < 12:
            hours += 12

        # Créer un objet time
        time_obj = time(hours,minutes,00)
        print(time_obj)
        return time_obj
    except ValueError as e:
        print(e)
        return None


@csrf_exempt 
def confirm_appointment(request):
    if request.method == 'POST':
        print(request.POST)
        try:

            patient_id = int(request.POST.get('patient_id'))
            doctor_id = int(request.POST.get('doctor_id'))
            date_str = request.POST.get('date')
            start_time_str = request.POST.get('start_time')
            end_time_str = request.POST.get('end_time')
            
            start_time = convert_time_string(start_time_str)
            end_time = convert_time_string(end_time_str)
            if start_time is None or end_time is None:
                raise ValueError('Invalid time format in start_time or end_time')

            print(f"start_time: {start_time}, end_time: {end_time}")

            appointment = Appointment.objects.create(
                patient_id=patient_id,
                doctor_id=doctor_id,
                date=date_str,
                start_time=start_time,
                end_time=end_time
            )

            print(appointment)
            messages.success(request, "Appointment confirmed ! Check your mailbox ")
            return JsonResponse({'status': 'success', 'message': 'Appointment confirmed successfully!'})

        except Exception as e:
            print(e)
        return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)



def get_doctors(request):
    speciality = request.GET.get('speciality', None)
    doctors = Doctor.objects.filter(speciality=speciality)
    
    context = {
        'doctors': doctors,
    }

    template_name = 'doctors_dropdown_options.html' if doctors else 'no_doctors_available.html'

    html = render_to_string(template_name, context)
    return JsonResponse({'html': html})

############################## ADMIN DASHBOARD ###########################################################

# - Dashboard

@login_required(login_url='home')
def dashboard(request):
    is_admin = request.user.is_staff

    if is_admin:
        doctors = Doctor.objects.all()
        patients = Patient.objects.all()
        appointments = Appointment.objects.all().order_by('date')

        return render(request, 'dashboard.html', {'doctors': doctors, 'patients': patients, 'appointments': appointments})
    else:
        return HttpResponse("Access Denied !")


@login_required(login_url='home')
def doc_dashboard(request):
    is_admin = request.user.is_staff

    if is_admin:
        doctors = Doctor.objects.all()
        return render(request, 'dashboard/Doctors_objects.html', {'doctors': doctors})
    else:
        return HttpResponse("Access Denied !")

@login_required(login_url='home')
def pat_dashboard(request):
    is_admin = request.user.is_staff

    if is_admin:
        patients = Patient.objects.all()
        return render(request, 'dashboard/Patients_objects.html', {'patients': patients})
    else:
        return HttpResponse("Access Denied !")

@login_required(login_url='home')
def app_dashboard(request):
    is_admin = request.user.is_staff

    if is_admin:
        appointments = Appointment.objects.all()
        return render(request, 'dashboard/Appointment_objects.html', {'appointments': appointments})
    else:
        return HttpResponse("Access Denied !")

@login_required(login_url='home')
def create_record(request):
    pass

######################### PATIENT PROFIL ######################################

@admin_forbiden
@login_required(login_url='home')  
def show_patient_appointment(request):
    if request.user.is_patient:
        patient_appointments = Appointment.objects.filter(patient_id=request.user.id)
        return render(request, 'patient_appointments.html', {'appointments': patient_appointments})
    else:
        # Gérer le cas où l'utilisateur connecté n'est pas un patient
        return HttpResponse("You are not authorized to view this page.")

@admin_forbiden
@login_required(login_url='home')  
def edit_patient_profil(request):
    pass    