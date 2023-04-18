from django import forms
from .models import User, Patient, Doctor
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

class UserRegisterForm(UserCreationForm):
    
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PatientSignUpForm(UserCreationForm):

    email = forms.EmailField()
    age = forms.IntegerField()
    gender = forms.CharField(max_length=1)

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_patient = True
        user.save()

        pat_name = self.cleaned_data.get("patient_name")
        pat_age = self.cleaned_data.get("age")
        pat_gender = self.cleaned_data.get("gender")
        # patient = Patient.objects.create(patient_name=user)
        pat_record = Patient(patient_name=pat_name, age=pat_age, gender=pat_gender)
        pat_record.save()
        return user
    


class DoctorSignUpForm(UserCreationForm):
    
    email = forms.EmailField()
    gender = forms.CharField(max_length=1)
    speciality = forms.CharField(max_length=20)
    city = forms.CharField(max_length=20)
    State = forms.CharField(max_length=20)
    date_of_joining = forms.DateField()
    
    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_doctor = True
        user.save()
        
        doc_name = self.cleaned_data.get("username")
        doc_mail = self.cleaned_data.get("email")
        doc_spec = self.cleaned_data.get("speciality")
        doc_city = self.cleaned_data.get("city")
        doc_state = self.cleaned_data.get("State")
        doj = self.cleaned_data.get("date_of_joining")
        doc_gender = self.cleaned_data.get("gender")
        doc_record = Doctor(doctor_name=doc_name, email=doc_mail, speciality=doc_spec, city=doc_city, State=doc_state, date_of_joining=doj , gender=doc_gender)
        doc_record.save()

        return user