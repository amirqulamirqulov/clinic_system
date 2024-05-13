from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import Specialization, User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Appoinment, Prescription
from .forms import AppoinmentForm, PrescriptionForm, DoctorForm, PatientForm, AdminForm, SpecializationForm, ContactForm
from django.urls import reverse_lazy, reverse
import datetime as dt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test


class HomePageView(ListView):
    model = Specialization
    template_name = "hospital/index.html"
    context_object_name = "specializations"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Specialization.objects.all()[:3]
        return queryset


class AboutView(ListView):
    model = User
    template_name = "hospital/about_us.html"
    context_object_name = "doctors"

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = User.objects.filter(role="doctor")[:4]
        return queryset
    

class ContactPageView(TemplateView):
    template_name = 'hospital/contact_us.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }
        return render(request, 'hospital/contact_us.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
       
        if form.is_valid() and request.method == "POST":
            form.save()
            return HttpResponse("<h2> Biz bilan bog'langaningiz uchun tashakkur!</h2>")
        else:
            return HttpResponse("<h4> Siz formani xato to'ldirdingiz! </h4>")
        


class ServicePageView(ListView):
    model = Specialization
    template_name = "hospital/services.html"
    context_object_name = "specializations"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Specialization.objects.all()
        return queryset



class AppoinmentView(ListView):
    model = Appoinment
    template_name = "pages/appoinment.html"
    context_object_name = "appointments"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        time_now = dt.datetime.now()
        if self.request.user.role == 'doctor':
            appoinments = Appoinment.objects.filter(datetimes__gt=time_now, doctor=self.request.user.id)
            role = 'doctor'
        elif self.request.user.role == 'patient':
            appoinments = Appoinment.objects.filter(datetimes__gt=time_now, patient=self.request.user.id)
            role = 'patient'
        context["appointments"] = appoinments
        context['count_appoinments'] = appoinments.count()
        context['role'] = role
        return context
    
def is_patient(user):
    return user.role == 'patient'


@login_required   
@user_passes_test(is_patient)
def createappoinmentview(request):
    if request.method == 'POST':
        form = AppoinmentForm(request.POST)
        if form.is_valid():
            doctor = form.cleaned_data['doctor']
            datetime = form.cleaned_data['datetimes']
            time = datetime.time()
            print(time)
            date = datetime.date()
            times = Appoinment.objects.filter(datetimes__date=date, doctor__username=doctor)
            delta = dt.timedelta(hours=1)
            delta1 = dt.timedelta(hours=5)
            for time1 in times:
                record_time = dt.datetime.combine(date, time1.datetimes.time())
                if ((record_time + delta1) - delta).time() < time < ((record_time + delta1) + delta).time():      
                    return HttpResponse('Bu vaqtda band qilingan')
            form.instance.patient = request.user
            form.instance.price = User.objects.get(username=doctor).price
            form.save()
            return redirect('appoinment')
    else:
        form = AppoinmentForm()
    return render(request, 'crud/add_appoinment.html', {'form': form})


def updateappoinmentview(request, pk):
    instance = get_object_or_404(Appoinment, pk=pk)

    if request.method == 'POST':
        form = AppoinmentForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return redirect('appoinment')
    else:
        form = AppoinmentForm(instance=instance)
        return render(request, 'crud/update_appoinment.html', {'form': form})

            


class DeleteAppoinmentView(DeleteView):
    model = Appoinment
    template_name = 'crud/delete_appoinment.html'
    context_object_name = 'appoinment'
    success_url = reverse_lazy('appoinment')



class PrescriptionView(ListView):
    model = Prescription
    template_name = 'pages/prescription.html'
    context_object_name = 'prescriptions'


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.user.role == 'doctor':
            prescription = Prescription.objects.filter(doctor=self.request.user.id)
            role = 'doctor'
        elif self.request.user.role == 'patient':
            prescription = Prescription.objects.filter(patient=self.request.user.id)
            role = 'patient'
        context['count_prescriptions'] =prescription.count()
        context['prescriptions'] = prescription
        context['role'] = role

        return context


class DeletePrescriptionView(DeleteView):
    model = Prescription
    template_name = 'crud/delete_prescription.html'
    context_object_name = 'prescription'
    success_url = reverse_lazy('prescription')


def updateprescriptionview(request, pk):
    instance = get_object_or_404(Prescription, pk=pk)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return redirect('prescription')
    else:
        form = PrescriptionForm(instance=instance)
        return render(request, 'crud/update_prescription.html', {'form': form})
    

def createprescriptionview(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.instance.doctor = request.user
            form.save()
            return redirect('prescription')
    else:
        form = PrescriptionForm()
    return render(request, 'crud/create_prescription.html', {'form': form})


class CreateDoctorView(CreateView):
    model = User
    form_class = DoctorForm
    template_name = 'crud/create_doctor.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)
    

    def get_success_url(self):
        return reverse('admin_page') 
    

class UpdateDoctorView(UpdateView):
    model = User
    form_class = DoctorForm
    template_name = 'crud/update_doctor.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('admin_page') 
    
class DeleteDoctorView(DeleteView):
    model = User
    template_name = 'crud/delete_doctor.html'
    success_url = reverse_lazy('admin_page')


class UpdatePatientView(UpdateView):
    model = User
    form_class = PatientForm
    template_name = 'crud/update_patient.html'

    def get_success_url(self):
        return reverse('admin_page') 
    
class DeletePatientView(DeleteView):
    model = User
    template_name = 'crud/delete_patient.html'
    success_url = reverse_lazy('admin_page')


class CreateAdminView(CreateView):
    model = User
    form_class = AdminForm
    template_name = 'crud/create_admin.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)
    

    def get_success_url(self):
        return reverse('admin_page') 
    

class UpdateAdminView(UpdateView):
    model = User
    form_class = AdminForm
    template_name = 'crud/update_admin.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('admin_page') 


class CreateSpecializationView(CreateView):
    model = Specialization
    form_class = SpecializationForm
    template_name = 'crud/create_specialization.html'

    def get_success_url(self) -> str:
        return reverse('admin_page')


class UpdateSpecializationView(UpdateView):
    model = Specialization
    form_class = SpecializationForm
    template_name = 'crud/update_specialization.html'

    def get_success_url(self):
        return reverse('admin_page') 
    
class DeleteSpecializationView(DeleteView):
    model = Specialization
    template_name = 'crud/delete_specialization.html'
    success_url = reverse_lazy('admin_page')


def doctor_list(request, specialization):
    doctors = User.objects.filter(specialization__name=specialization, role='doctor')
    context = {
        'doctors' : doctors,
        'specialization': specialization
    }
    return render(request, 'pages/doctor_list.html', context=context)

