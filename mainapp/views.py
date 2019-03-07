from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .forms import BarberLoginForm

# Create your views here.


def home(request):
    return render(request, 'home.html')


def barber_login(request):
    if request.POST:
        login_form = BarberLoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                redirect('mainapp:home')
            else:
                # Return an 'invalid login' error message.
                # ...
                pass

    else:
        return render(request, 'login.html')


def barber_logout(request):
    logout(request)
    return render(request, 'home.html')


def barber_profile(request):
    pass
