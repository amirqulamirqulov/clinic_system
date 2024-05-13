from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *
# Register your models here.


# admin.site.register(Department)
# admin.site.register(Country)


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

# @admin.register(Region)
# class RegionAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'country')

# @admin.register(District)
# class DistrictAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_superuser")
    search_fields = ("username", "first_name", "last_name", "email")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "username", "role",  "specialization", 'price', "user_address", "phone_number", "image", "date_of_birth", "gender")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    # "groups",
                    # "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

@admin.register(VerificationOTP)
class VerificationOtpAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code', 'expires_in', 'is_active')




