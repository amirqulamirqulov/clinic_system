from django.urls import path
from .views import *
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    path('admin/', adminpageview, name="admin_page"),
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name='logout'),
    path('profile/', dashbord_user, name='user_profile'),
    path('profile/update/', UpdateUserView.as_view(), name='update_user'),
    path('profile/password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('profile/password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('profile/password-reset/', password_reset, name='password_reset'),
    path('profile/password-reset/done/', otp_view, name='password_reset_done'),
    path('profile/password-reset/confirm/', password_confirm, name='password_reset_confirm'),
    path('profile/password-reset/complete/', password_complete, name='password_reset_complete'),
    path('register/email-verify/', password_reset_email, name='password_verify_email'),
    path('register/complete/<uidb64>/<token>/', activate, name='register_complete')  
]
