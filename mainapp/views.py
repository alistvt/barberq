from django.shortcuts import render
from django.contrib.auth import logout
# Create your views here.


def home(request):
    return render(request, 'home.html')


def barber_login(request):
    return render(request, 'login.html')


def barber_logout(request):
    logout(request)
    return render(request, 'home.html')


def barber_profile(request):
    pass
