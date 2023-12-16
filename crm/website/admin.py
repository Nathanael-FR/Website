
# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Patient, Doctor, Appointment, Availability
from django.utils.translation import gettext_lazy as _

class PatientAdminForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput)
    
    class Meta:
        model = Patient
        fields = ('email', 'first_name', 'last_name', 'phone_number')

class PatientAdmin(admin.ModelAdmin):
    form = PatientAdminForm

    def save_model(self, request, obj, form, change):
        # Créer un CustomUser lors de la sauvegarde du Patient
        user = CustomUser.objects.create_user(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name']
        )
        obj.user = user
        obj.save()

admin.site.register(Patient, PatientAdmin)

class DoctorAdminForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput)
    
    class Meta:
        model = Doctor
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'speciality')

class DoctorAdmin(admin.ModelAdmin):
    form = DoctorAdminForm

    def save_model(self, request, obj, form, change):
        # Créer un CustomUser lors de la sauvegarde du Doctor
        user = CustomUser.objects.create_user(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name']
        )
        obj.user = user
        obj.save()

admin.site.register(Doctor, DoctorAdmin)

admin.site.register(Appointment)
admin.site.register(Availability)
admin.site.register(CustomUser)