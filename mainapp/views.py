from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError
from .forms import BarberLoginForm
from .models import Barbery, Reservation

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


@login_required
def barber_logout(request):
    logout(request)
    return render(request, 'home.html')


@login_required
def barber_profile(request):
    pass


@login_required
def add_slot(request):
    pass


@login_required
def manage_slots(request):
    pass


@login_required
def view_reserves(request):
    now = datetime.now()
    barbery = Barbery.objects.get(username=request.user.username)
    passed_reserves = barbery.time_slots.filter(reserved=True, start_time__lt=now).order_by('-start_time')
    upcoming_reserves = barbery.time_slots.filter(reserved=True, start_time__gte=now).order_by('start_time')
    return render(request, 'view_reserveds.html', {'passed_reserves': passed_reserves,
                                                   'upcoming_reserves': upcoming_reserves, })
