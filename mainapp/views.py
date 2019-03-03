from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home.html')


def barber_login(request):
    return render(request, 'templates/login.html')
