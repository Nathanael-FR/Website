#models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

SPECIALITY_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('endocrinology', 'Endocrinology'),
        ('gastroenterology', 'Gastroenterology'),
        ('hematology', 'Hematology'),
        ('neurology', 'Neurology'),
        ('oncology', 'Oncology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('psychiatry', 'Psychiatry'),
    ]

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    def is_doctor(self):
        return hasattr(self, 'doctor')

    def is_patient(self):
        return hasattr(self, 'patient')
    

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.IntegerField()
    speciality = models.CharField(max_length=20, choices=SPECIALITY_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self) :
        return f"{self.doctor} : {self.patient} | {self.date} : from {self.start_time} to {self.end_time}"
    
class Availability(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING)
    
    class Meta:
        verbose_name_plural = "Availabilities"
    
    def __str__(self) -> str:
        return f'{self.date} : from {self.start_time} to {self.end_time} \n Doc : {self.doctor}'