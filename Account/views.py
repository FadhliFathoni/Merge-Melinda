from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages

from django.contrib.auth import get_user_model

Account = get_user_model()

# Create your views here.


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        if Account.objects.filter(email=email).exists():
            messages.info(request, 'email is already exist')
            return redirect(register)
        else:
            user = Account.objects.create_user(
                password=password, email=email, phone=phone, name=name)
            user.set_password(password)
            user.save()
            return redirect('login_user')
    else:
        print("this is not post method")
        return render(request, "register.html")


def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid email or password')
            return redirect('login_user')

    else:
        return render(request, "login.html")


def logout_user(request):
    auth.logout(request)
    return redirect('home')
