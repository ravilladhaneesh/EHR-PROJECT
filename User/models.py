from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    is_admin = models.BooleanField("is admin" ,default=False)
    is_patient = models.BooleanField("is patient" ,default=True)
    is_doctor = models.BooleanField("is doctor" ,default=False)


class Patient(models.Model):
    patient_name = models.OneToOneField(User, related_name="patient", on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return f'{self.patient_name}'
    
    
# class Doctor(models.Model):
#     doctor_name = models.OneToOneField(User, related_name="doctor", on_delete=models.CASCADE, primary_key=True)

#     def __str__(self):
#         return f'{self.doctor_name}'
