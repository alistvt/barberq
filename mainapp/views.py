from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError
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
                return redirect('mainapp:home')
            else:
                login_form.add_error(password, ValidationError(_('Password doesn\'t match with username!')))
    else:
        login_form = BarberLoginForm()

    return render(request, 'login.html', {'form': login_form})


def barber_logout(request):
    logout(request)
    return render(request, 'home.html')


def barber_profile(request):
    pass
