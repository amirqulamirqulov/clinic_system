from django.shortcuts import render, redirect
from .models import User, Specialization
from .forms import UserRegisterForm, LoginForm, UpdateUserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views import View


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
            new_user.save()
            
            return redirect('login') 
    else:
        form = UserRegisterForm()
    return render(request, 'registration/user_register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
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
        

