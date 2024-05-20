from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView, \
    PasswordChangeDoneView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView


urlpatterns = [
    path('admin/', adminpageview, name="admin_page"),
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name='logout'),
    path('profile/', dashbord_user, name='user_profile'),
    path('profile/update/', UpdateUserView.as_view(), name='update_user'),
    path('profile/password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('profile/password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('profile/password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('profile/password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('profile/password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete')
]
