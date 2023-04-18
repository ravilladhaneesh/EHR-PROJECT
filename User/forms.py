from django import forms
from .models import User, Patient
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

class UserRegisterForm(UserCreationForm):
    
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PatientSignUpForm(UserCreationForm):

    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_patient = True
        user.save()

        patient = Patient.objects.create(patient_name=user)
        return user
    


# class DoctorSignUpForm(UserCreationForm):
    
#     email = forms.EmailField()
    
#     class Meta(UserCreationForm.Meta):
#         model = User
    
#     @transaction.atomic
#     def save(self):
#         user = super().save(commit=False)
#         user.is_doctor = True
#         user.save()

#         doctor = Doctor.objects.create(doctor_name=user)
#         return user