# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Patient, Doctor

@receiver(post_save, sender=Patient)
def assign_patient_role(sender, instance, created, **kwargs):
    if created:
        instance.user.is_patient = True
        instance.user.save()


@receiver(post_save, sender=Doctor)
def assign_patient_role(sender, instance, created, **kwargs):
    if created:
        instance.user.is_doctor = True
        instance.user.save()
