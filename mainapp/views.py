from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import BarberLoginForm, AddSlotsForm, BarberyUpdateProfileForm, TimeSlotDeleteForm
from .models import Barbery, TimeSlot
from .list_filters import ReservationFilter

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
        add_slot_form = AddSlotsForm(barbery, request.POST)
        if add_slot_form.is_valid():
            cd = add_slot_form.cleaned_data
            TimeSlot.create_bulk(start_time=cd['start_time'],
                                 duration=timedelta(hours=cd['duration_hours'], minutes=cd['duration_minutes']),
                                 add_for_a_week=cd['add_for_a_week'],
                                 barbery=barbery)
            return render(request, 'add_slots.html', {'form': AddSlotsForm(barbery), 'success': True})
        else:
            return render(request, 'add_slots.html', {'form': add_slot_form})
    add_slot_form = AddSlotsForm(barbery)
    return render(request, 'add_slots.html', {'form': add_slot_form})


@login_required
def manage_slots(request):
    barbery = Barbery.objects.get(username=request.user.username)
    time_slots = barbery.time_slots.all().order_by('-start_time')
    success = None
    filter_data = ReservationFilter(request.GET)
    if request.POST:
        form = TimeSlotDeleteForm(barbery, request.POST)
        if form.is_valid():
            form.save()
        time_slots = barbery.time_slots.all().order_by('-start_time')
        success = True
    else:
        if request.GET.get('search', None):
            time_slots = time_slots.filter(reserved=True, reservation__user__email__icontains=request.GET['search'])

    return render(request, 'manage_slots.html', {'slots': time_slots, 'success': success, 'filter': filter_data})


@login_required
def view_reserves(request):
    now = datetime.now()
    barbery = Barbery.objects.get(username=request.user.username)
    passed_reserves = barbery.time_slots.filter(reserved=True, start_time__lt=now).order_by('-start_time')
    upcoming_reserves = barbery.time_slots.filter(reserved=True, start_time__gte=now).order_by('start_time')
    return render(request, 'view_reserveds.html', {'passed_reserves': passed_reserves,
                                                   'upcoming_reserves': upcoming_reserves, })
