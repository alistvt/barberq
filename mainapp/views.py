from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError
from .forms import BarberLoginForm, AddSlotsForm, BarberyUpdateProfileForm
from .models import Barbery, Reservation, TimeSlot

# Create your views here.


def home(request):
    return render(request, 'home.html')


def barber_login(request):
    if request.POST:
        login_form = BarberLoginForm(request.POST)
        if login_form.is_valid():
                login(request, login_form.user)
                return redirect('mainapp:home')
    else:
        login_form = BarberLoginForm()

    return render(request, 'login.html', {'form': login_form})


@login_required
def barber_logout(request):
    logout(request)
    return render(request, 'home.html')


@login_required
def barber_profile(request):
    barber = Barbery.objects.get(id=request.user.id)
    if request.POST:
        profile_form = BarberyUpdateProfileForm(request.POST, instance=barber)
        if profile_form.is_valid():
            profile_form.save()
            return render(request, 'update_profile.html', {'form': profile_form, 'success': True})
        else:
            return render(request, 'update_profile.html', {'form': profile_form})

    profile_form = BarberyUpdateProfileForm(instance=barber)
    return render(request, 'update_profile.html', {'form': profile_form})


@login_required
def add_slot(request):
    barbery = Barbery.objects.get(id=request.user.id)
    if request.POST:
        add_slot_form = AddSlotsForm(request.POST)
        if add_slot_form.is_valid():
            cd = add_slot_form.cleaned_data
            TimeSlot.create_bulk(start_time=cd['start_time'],
                                 duration=timedelta(hours=cd['duration_hours'], minutes=cd['duration_minutes']),
                                 add_for_a_week=cd['add_for_a_week'],
                                 barbery=barbery)
            return render(request, 'add_slots.html', {'form': AddSlotsForm(), 'success': True})
        else:
            return render(request, 'add_slots.html', {'form': add_slot_form})
    add_slot_form = AddSlotsForm()
    return render(request, 'add_slots.html', {'form': add_slot_form})


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
