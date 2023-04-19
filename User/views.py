from django.shortcuts import render, redirect
from .forms import UserRegisterForm, PatientSignUpForm, DoctorSignUpForm, AppointmentForm
from django.contrib import messages
from django.contrib.auth import login
from django.views.generic import CreateView
from .models import User
from django.contrib.auth.decorators import login_required
from .decorators import patient_required, admin_required
from django.utils.decorators import method_decorator
from .models import Doctor, Patient, Appointment

# Create your views here.

def home(request):
    context = {
        'doctor': Doctor.objects.all(),
        'patient': Patient.objects.all(),
        'appointment': Appointment.objects.all(),
    }
    return render(request, 'User/doctors.html', context)


def register(request):
    if request.method =="POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}')
            return redirect('main-home')
    else:
        form = UserRegisterForm()
        return render(request, 'User/register.html', {"form": form})


class PatientSignUpView(CreateView):
    model = User
    form_class = PatientSignUpForm
    context_object_name = 'form'
    template_name = "User/register.html"
    

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = 'patient'
        return super().get_context_data(**kwargs)

    def form_valid(self,form):
        user = form.save()
        messages.success(self.request, f"Created Account for {form.cleaned_data.get('username')}")
        # login(self.request, user)
        return redirect('login')


@login_required
@patient_required
def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            patient_name = form.cleaned_data.get('patient_name')
            messages.success(request,f'Appointment booked for {patient_name}')
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