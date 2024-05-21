from django.shortcuts import render, redirect
from .models import User, Specialization, VerificationOTP
from .forms import UserRegisterForm, LoginForm, UpdateUserForm, VerificationOTPForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views import View
from .utils import send_otp
from django.core.mail import send_mail
from core import settings
import datetime
import pyotp
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

def adminpageview(request):
    doctors = User.objects.filter(role="doctor")
    patients = User.objects.filter(role="patient")
    admins = User.objects.filter(role="admin")
    specializations = Specialization.objects.all()
    count_doctors = doctors.count()
    count_patients = patients.count()
    count_admins = admins.count()
    count_specializations = specializations.count()
    context = {
        "doctors" : doctors,
        "patients" : patients,
        "admins" : admins,
        "specializations" : specializations,
        "count_doctors": count_doctors,
        "count_patients": count_patients,
        "count_admins": count_admins,
        "count_specializations": count_specializations
    }

    return render(request, "pages/admin.html", context=context)


def user_register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
               
                return HttpResponse('Bu username yoki email avval ham ishlatilgan')
        
            new_user = User.objects.create_user(username=username, email=email, password=password)
            
            
            new_user.role = "patient"
            new_user.is_active = False
            new_user.save()
            
            send_verification_email(request=request, user=new_user)
            
            return redirect('password_verify_email') 
    else:
        form = UserRegisterForm()
    return render(request, 'registration/user_register.html', {'form': form})


def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = request.build_absolute_uri(
        reverse('register_complete', kwargs={'uidb64': uidb64, 'token': token})
    )

    subject = 'Email tasdiqlash'
    message = f'Profilingizni tasdiqlash uchun linkka kiring:\n\n{verification_url}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return HttpResponse('Faollashtirish havolasi yaroqsiz!')
    
def password_reset_email(request):
    return render(request, 'registration/password_reset_email.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return HttpResponse('Sizning profilingiz faol holatda emas!')
            else:
                return HttpResponse('Username yoki passwordda xatolik bor.')
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})
    

def user_logout(request):
    logout(request=request)
    return render(request, 'registration/logged_out.html')


def dashbord_user(request):
    user = User.objects.get(id=request.user.id)
    context = {
        'user': user
    }
    return render(request, 'pages/profile.html', context=context)

class UpdateUserView(View):
    def get(self, request):
        user_form = UpdateUserForm(instance=request.user)
        context = {
            'user_form' : user_form
        }
        return render(request, 'pages/update_user.html', context=context)
    
    def post(self, request):
        user_form = UpdateUserForm(instance=request.user, data=request.POST, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            return redirect('user_profile')
        else:
            return HttpResponse("Siz ma'lumotni noto'g'ri kiritdingiz.")
        


def password_reset(request):
    if request.method == 'POST':
        form = VerificationOTPForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                request.session['email'] = email
                code = send_otp(request=request)
                subject = 'Email tasdiqlash.'
                message = f'Parolni tiklash uchun tasdiqlash kodi:  {code}'
                from_email = settings.EMAIL_HOST_USER
                expires_in = request.session['otp_valid_date']
                VerificationOTP.objects.create(email=email, code=code, expires_in=expires_in)
                recipient_list = [email]

                send_mail(subject, message, from_email, recipient_list)
                return redirect('password_reset_done')
            else:
                return HttpResponse("Bu emaildan avval ro'yxatdan o'tilmagan")
    else:
        form = VerificationOTPForm()
        return render(request, 'registration/password_reset_form.html', {'form':form})
    

def otp_view(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']
        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.datetime.fromisoformat(otp_valid_date)
            if valid_until > datetime.datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=180)
                if totp.verify(otp=otp):
                    return redirect('password_reset_confirm')
    return render(request, 'registration/password_reset_done.html', {})


def password_confirm(request):
    email = request.session['email']
    user = User.objects.get(email=email)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_reset_complete')
    else:
        form = SetPasswordForm(user, request.GET)
        return render(request, 'registration/password_reset_confirm.html', {'form': form})


def password_complete(request):
    return render(request, 'registration/password_reset_complete.html')



        

