from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Appoinment(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appoinment_doctors')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appoinment_patients')
    datetimes = models.DateTimeField(_("datetimes"), null=True, blank=True)
    price = models.IntegerField(_("price"))
    status = models.BooleanField(_("status"), default=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} | {self.datetimes}"
    
    class Meta:
        verbose_name = _("appoinment")
        verbose_name_plural = _("appoinments")

class Prescription(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescription_doctors')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescription_patients')
    datetime = models.DateTimeField(_("datetime"))
    text = models.TextField(_("text"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} | {self.datetime}"
    
    class Meta:
        verbose_name = _("prescription")
        verbose_name_plural = _("prescriptions")
    
# class Treatment(models.Model):
#     name = models.CharField(_("name"), max_length=60)
#     price = models.IntegerField(_("price"))
#     created_at = models.DateTimeField(_("created at"), auto_now_add=True)
#     updated_at = models.DateTimeField(_("updated at"), auto_now=True)

#     def __str__(self) -> str:
#         return self.name
    
#     class Meta:
#         verbose_name = _("treatment")
#         verbose_name_plural = _("treatments")


# class TreatmentService(models.Model):
#     doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='treatment_service_doctors')
#     patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='treatment_service_patients')
#     treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name="treatment_services")
#     paid_fee = models.IntegerField(_("paid fee"))
#     status = models.BooleanField(_("status"), default=False)


    # def __str__(self) -> str:
    #     return f"{self.doctor.first_name} | {self.patient.first_name}"
    
    # class Meta:
    #     verbose_name = _("treatment service")
    #     verbose_name_plural = _("treatment services")


class Contact(models.Model):
    name = models.CharField(_('name'), max_length=50)
    email = models.CharField(_('email'), max_length=50)
    phone_number = models.IntegerField(_('phone number'))
    message = models.TextField(_('message'))

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = ('contacts')