from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, PatientSignUpForm
from django.contrib import messages
from django.contrib.auth import login
from django.views.generic import CreateView
from .models import User
from django.contrib.auth.decorators import login_required
from .decorators import patient_required

# Create your views here.

def home(request):
    return render(request, 'User/home.html')


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
        login(self.request, user)
        return redirect('login')


@login_required
@patient_required
def book_appointment(request):
    return render(request, 'User/home.html')

# class DoctorSignUpView(CreateView):
#     model = User
#     form_class = DoctorSignUpForm
#     context_object_name = 'form'
#     template_name = "User/register.html"
    

#     def get_context_data(self, **kwargs):
#         kwargs["user_type"] = 'doctor'
#         return super().get_context_data(**kwargs)

#     def form_valid(self,form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('main-home')
