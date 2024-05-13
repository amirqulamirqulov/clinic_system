from django.urls import path 
from .views import *


urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('about/', AboutView.as_view(), name="about"),
    path('contact/', ContactPageView.as_view(), name="contact"),
    path('services/', ServicePageView.as_view(), name="services"),
    path('appoinment/', AppoinmentView.as_view(), name="appoinment"),
    path('appoinment/<int:pk>/delete/', DeleteAppoinmentView.as_view(), name='delete_appo'),
    path('appoinment/<int:pk>/update/', updateappoinmentview, name='update_appo'),
    path('appoinment/create/', createappoinmentview, name='create_appo'),
    path('prescription/<int:pk>/delete/', DeletePrescriptionView.as_view(), name='delete_prescrip'),
    path('prescription/<int:pk>/update/', updateprescriptionview, name='update_prescrip'),
    path('prescription/', PrescriptionView.as_view(), name='prescription'),
    path('prescription/create/', createprescriptionview, name='create_prescrip'),
    path('doctor/create/', CreateDoctorView.as_view(), name='create_doctor'),
    path('doctor/<int:pk>/update/', UpdateDoctorView.as_view(), name='update_doctor'),
    path('doctor/<int:pk>/delete/', DeleteDoctorView.as_view(), name='delete_doctor'),
    path('patient/<int:pk>/update/', UpdatePatientView.as_view(), name='update_patient'),
    path('patient/<int:pk>/delete/', DeletePatientView.as_view(), name='delete_patient'),
    path('admins/new/', CreateAdminView.as_view(), name='create_admin'),
    path('admins/<int:pk>/update/', UpdateAdminView.as_view(), name='update_admin'),
    path('specialization/create/', CreateSpecializationView.as_view(), name='create_speci'),
    path('specialization/<int:pk>/update/', UpdateSpecializationView.as_view(), name='update_speci'),
    path('specialization/<int:pk>/delete/', DeleteSpecializationView.as_view(), name='delete_speci'),
    path('specialization/<str:specialization>/doctors/', doctor_list, name='doctor_list')
]


