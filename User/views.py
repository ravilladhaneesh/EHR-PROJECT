from django.shortcuts import render, redirect
from .forms import UserRegisterForm, PatientSignUpForm, DoctorSignUpForm, AppointmentForm, ConsultForm
from django.contrib import messages
from django.contrib.auth import login
from django.views.generic import CreateView
from .models import User
from django.contrib.auth.decorators import login_required
from .decorators import patient_required, admin_required, doctor_required
from django.utils.decorators import method_decorator
from .models import Doctor, Patient, Appointment, Consult
from django.views.generic import DetailView, ListView , View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

def home(request):
    context = {
        'doctor': Doctor.objects.all(),
        'patient': Patient.objects.all(),
        'appointment': Appointment.objects.all(),
    }
    return render(request, 'User/doctors.html', context)


# def register(request):
#     if request.method =="POST":
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request,f'Account created for {username}')
#             return redirect('main-home')
#     else:
#         form = UserRegisterForm()
#         return render(request, 'User/register.html', {"form": form})


class PatientSignUpView(CreateView):
    model = User
    form_class = PatientSignUpForm
    context_object_name = 'form'
    template_name = "User/register.html"
    

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = 'patient'
        return super().get_context_data(**kwargs)

    def form_valid(self,form):
        form.save()
        messages.success(self.request, f"Created Account for {form.cleaned_data.get('username')}")
        # login(self.request, user)
        return redirect('login')


@login_required
@patient_required
def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            doctor_name = form.cleaned_data.get('doctor_name')
            messages.success(request,f'Appointment booked for {doctor_name}')
            return redirect('main-home')
    else:
        form = AppointmentForm()
    
    return render(request, 'User/register.html', {"form": form})
        



@method_decorator(login_required, name="dispatch")
@method_decorator(admin_required, name="dispatch")
class DoctorSignUpView(  CreateView):
    model = User
    form_class = DoctorSignUpForm
    context_object_name = 'form'
    template_name = "User/register.html"
    
    def get_context_data(self, **kwargs):
        kwargs["user_type"] = 'doctor'
        return super().get_context_data(**kwargs)

    
    def form_valid(self,form):
        user = form.save()
        messages.success(self.request, f"Created Account for {form.cleaned_data.get('username')}")
        # login(self.request, user)
        return redirect('main-home')



@login_required
@admin_required
def dashboard(request):
    context = {
        'doctor': Doctor.objects.all(),
        'patient': Patient.objects.all(),
        'appointment': Appointment.objects.all(),
    }
    return render(request, 'User/dashboard.html', context)


@login_required
def view_patients(request):
    context = {
        'patient': Patient.objects.all(),
    }

    return render(request, "User/patients.html", context )


@login_required
def view_doctors(request):
    context = {
        'doctor': Doctor.objects.all(),
    }

    return render(request, "User/doctors.html", context )

@login_required
@admin_required
def view_appointments(request):
    context = {
        'appointment': Appointment.objects.all(),
    }

    return render(request, 'User/appointments.html', context)



class DoctorDetailView(LoginRequiredMixin, DetailView):
    model = Doctor

@login_required
@doctor_required
def appointment_patient(request):
    context = {
        'appointment': Appointment.objects.filter(doctor_name=request.user.username),
        # 'user_name' : request.user,
    }
    return render(request, 'User/view_patient.html', context )


class AppointmentDetialView(LoginRequiredMixin , DetailView):
    model =  Appointment
    

@login_required    
def profile(request):
    return render(request, 'User/profile.html')


@login_required
@doctor_required
def consult_patient(request):
    if request.method == "POST":
        form = ConsultForm(request.POST, request.FILES)
        file = request.FILES["file"]
        
        if form.is_valid():
            
            file = request.FILES["file"]
            msg = form.save(request)
            pat_name = form.cleaned_data.get("patient_name")
            doc_name = form.cleaned_data.get("doctor_name")
            messages.success(request, msg)
            return redirect('appointment-patient')
        
    else:
        form = ConsultForm()

    return render(request, "User/consult.html", {"form": form})
        


@login_required
@patient_required
def view_patient_record(request):
    user = request.user.username
    context = {
        'consult': Consult.objects.filter(patient_name=user)
    }

    return render(request, 'User/view_patient_record.html', context )