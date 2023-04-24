from django import forms
from .models import User, Patient, Doctor, Appointment, Consult
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
        user.email = self.cleaned_data.get("email")
        user.save()

        pat_name = self.cleaned_data.get("username")
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
    date_of_joining = forms.DateField(widget=forms.DateInput(
            attrs={
                    'placeholder': 'YYYY-MM-DD', 'required': 'required'
                  }
            ))
    
    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_doctor = True
        user.email = self.cleaned_data.get("email")
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
    

class AppointmentForm(forms.Form):

    
    doctor_name = forms.CharField(max_length=20)
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                    'placeholder': 'YYYY-MM-DD', 'required': 'required'
                  }
            )
        )
    time = forms.TimeField(
        widget=forms.DateInput(
            attrs={
                    'placeholder': 'HH:MM:SS', 'required': 'required'
                  }
            )
        )


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AppointmentForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Appointment

    def save(self):
        data = self.cleaned_data

        doc_name = data["doctor_name"]
        app_date = data["date"]
        app_time = data["time"]
        doc_obj = Doctor.objects.get(pk=doc_name)
        # print("-------------------------------------------------",self.user.username)
        
        pat_obj = Patient.objects.get(pk=self.user.username)
        # print("------------------------------------------------------------------------",pat_obj)
        appointment_record = Appointment(patient_name=pat_obj, doctor_name=doc_obj, date=app_date, time=app_time)
        appointment_record.save()



class ConsultForm(forms.Form):

    patient_name = forms.CharField(max_length=20)
    doctor_name = forms.CharField(max_length=20)
    description = forms.CharField(max_length=500)
    tablets = forms.CharField(max_length=100)
    tests = forms.CharField(max_length=100)
    file = forms.FileField()

    class Meta:
        model = Consult 
        # fields = ['doctor_name', 'patient_name', 'tablets', 'tests',  'description', 'file']

    
    def save(self, request):
        # doc_name = self.user.username
        
        data = self.cleaned_data

        pat_name = data["patient_name"]
        doc_name = data["doctor_name"]
        desc = data["description"]
        tabs = data["tablets"]
        test = data["tests"]
        fp = data["file"]

        pat_obj = Patient.objects.filter(patient_name=pat_name).first()
        doc_obj = Doctor.objects.get(pk=doc_name)

        consult_obj = Consult(patient_name=pat_obj, doctor_name=doc_obj, description=desc, tablets=tabs, tests=test, file=fp)


        app_obj = Appointment.objects.filter(patient_name=pat_obj)

        print(request.user.username,"----------------------------------------------")
        print(doc_name,"----------------------------------------------")

        if consult_obj and app_obj  :
            if request.user.username == doc_name:
                consult_obj.save()
                app_obj.delete()
                return f'Patient {pat_name} is consulted by doctor {doc_name}'
            else:
                return f'Patient {pat_name} does not booked appointment with Doctor {doc_name}'
            
        return f'Invalid consult fields or wrong Appointment .'