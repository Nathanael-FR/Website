# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Patient, CustomUser

class PatientSignUpForm(UserCreationForm):
    phone_number = forms.IntegerField()

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Adresse e-mail'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
            Patient.objects.create(user=user,first_name=user.first_name, last_name=user.last_name, phone_number=user.phone_number)
        return user

    
