from django import forms
from .models import Appoinment, Prescription, Contact
from accounts.models import User, Specialization


class AppoinmentForm(forms.ModelForm):
    class Meta:
        model = Appoinment
        fields = ['doctor', 'datetimes']


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'datetime', 'text']

class DoctorForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password_2 = forms.CharField(
        label="Password_confirm",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'role', 'specialization', 'date_of_birth', 'image', 'price', 'gender', 'email',]

    def clean_password_2(self):
        data = self.cleaned_data
        if data['password'] != data['password_2']:
            raise forms.ValidationError("Ikkala parolingiz ham bir biriga teng bo'lishi kerak")
        return data['password_2']


class PatientForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'date_of_birth', 'image', 'gender',]

class AdminForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password_2 = forms.CharField(
        label="Password_confirm",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'date_of_birth', 'image', 'gender', 'role', 'is_staff', 'is_superuser', 'email']

    def clean_password_2(self):
        data = self.cleaned_data
        if data['password'] != data['password_2']:
            raise forms.ValidationError("Ikkala parolingiz ham bir biriga teng bo'lishi kerak")
        return data['password_2']
    
class SpecializationForm(forms.ModelForm):
    class Meta:
        model = Specialization
        fields = ['name', 'description', 'image']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'