"""ehr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from User import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",user_views.home, name='main-home'),
    path("register/patient", user_views.PatientSignUpView.as_view(), name="patient-signup"),
    path('login/',auth_views.LoginView.as_view(template_name="User/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="User/logout.html"), name="logout"),
    path('profile', user_views.profile, name='profile'),
    path("appointment_patient/" , user_views.appointment_patient, name='appointment-patient'),
    path('appointment/', user_views.book_appointment, name="book-appointment"),
    path('register/doctor', user_views.DoctorSignUpView.as_view() , name="doctor-signup"),
    path('dashboard/', user_views.dashboard, name='dashboard'),
    path('view_patients/', user_views.view_patients, name="view-patients"),
    path('view_doctors/', user_views.view_doctors, name="view-doctors"),
    path('view_appointments/', user_views.view_appointments, name="view-appointments"),
    path('doctor/<str:pk>', user_views.DoctorDetailView.as_view(), name="doctor-detail"),
    path('patient/<str:pk>', user_views.AppointmentDetialView.as_view(), name="appointment-detail"),
    # path("consult/", user_views.ConsultCreateView.as_view(), name='consult-patient'),
    path("consult/", user_views.consult_patient, name='consult-patient'),
    path("view_patient_record/", user_views.view_patient_record, name="view-patient-record"),
    path("search_patient_record/", user_views.SearchPatientRecord.as_view(), name="search-patient-record"),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
