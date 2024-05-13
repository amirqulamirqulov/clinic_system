from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
# Register your models here.


@admin.register(Appoinment)
class AppoinmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'patient', 'datetimes', 'price', 'status', 'created_at')

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'patient', 'datetime', 'text', 'created_at')

# admin.site.register(Treatment)


# @admin.register(TreatmentService)
# class TreatmentServiceAdmin(admin.ModelAdmin):
#     list_display = ('id', 'doctor', 'patient', 'paid_fee', 'status')


