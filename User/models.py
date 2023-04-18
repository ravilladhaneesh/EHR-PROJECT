from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    is_admin = models.BooleanField("is admin" ,default=False)
    is_patient = models.BooleanField("is patient" ,default=False)
    is_doctor = models.BooleanField("is doctor" ,default=False)


class Patient(models.Model):
    patient_name = models.CharField(max_length=20, primary_key=True)
    age = models.IntegerField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    def __str__(self):
        return f'{self.patient_name}'
    
    
class Doctor(models.Model):
    doctor_name = models.CharField(max_length=20, primary_key=True)
    speciality = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    State = models.CharField(max_length=20)
    date_of_joining = models.DateField()
    email = models.EmailField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return f'{self.doctor_name}'
