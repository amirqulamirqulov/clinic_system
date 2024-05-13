from django.db import models
from django.utils.translation import gettext_lazy as _ 
from django.core.validators import RegexValidator, FileExtensionValidator
from django.contrib.auth.models import AbstractUser
# Create your models here.

    

class Specialization(models.Model):

    name = models.CharField(_("name"), max_length=250)
    description = models.TextField(_("description"))
    image = models.FileField(_("file"), upload_to="hospital/", validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("specialization")
        verbose_name_plural = _("specializations")




class User(AbstractUser):
    class UserType(models.TextChoices):
        DOCTOR = "doctor", _("doctor")
        PATIENT = "patient", _("patient")
        ADMIN = "admin", _("admin")

    class UserGender(models.TextChoices):
        MALE = "erkak", _("male")
        FEMALE = "ayol", _("female")

    
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    role = models.CharField(_("role"), max_length=10, choices=UserType.choices, default="patient")
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, related_name="specialization_users", null=True, blank= True)
    user_address = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(_("phone number"), max_length=20, validators=[RegexValidator(r'^998[012345789][0-9]{8}$')], null=True, blank=True)
    image = models.ImageField(_("image"), upload_to="users/", validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], null=True, blank=True)
    price = models.IntegerField(_("price"), null=True, blank=True)
    gender = models.CharField(_("gender"), max_length=10, choices=UserGender.choices, null=True, blank=True)
    

    def __str__(self) -> str:
        return self.username
    

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    
class VerificationOTP(models.Model):

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='verification_otp')
    code = models.IntegerField(_("otp code"))
    expires_in = models.DateTimeField(_("expires in"))
    is_active = models.BooleanField(_("is active"), default=True)


    def __str__(self) -> str:
        return f"{self.user.username}  | {self.code}"

    class Meta:
        verbose_name = _("verification otp")
        verbose_name_plural = _("verification otps")



