from datetime import date, datetime, timedelta
from django.utils import timezone
from django import forms
from django.forms import ModelForm, ValidationError, Form
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from tempus_dominus.widgets import DateTimePicker

from mainapp.models import Reservation, Barbery, TimeSlot


class BarberyCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    name = forms.CharField(max_length=100, required=True)
    address = forms.CharField(max_length=1000)

    class Meta:
        model = Barbery
        fields = ('name', 'email', 'password1', 'password2', 'first_name', 'last_name', 'address', 'is_active')

    def save(self, commit=True):
        barbery = super(BarberyCreationForm, self).save(commit=False)
        barbery.username = None
        # barbery.name = self.cleaned_data['name']
        # barbery.address = self.cleaned_data['address']

        barbery.save()

        return barbery


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['user', 'slot', ]

    def clean_slot(self):
        slot = self.cleaned_data['slot']
        if slot.reserved:
            raise ValidationError(_('This slot is reserved.'))
        return slot


class BarberLoginForm(Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                Barbery.objects.get(id=user.id)
                self.user = user
            except Barbery.DoesNotExist:
                raise ValidationError(_('Barber with these credential doesn\'t exist!'))
        else:
            raise ValidationError(_('Username and password don\'t match!'))


class AddSlotsForm(Form):
    start_time = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'minDate': (
                    date.today()
                ).strftime(
                    '%Y-%m-%d'
                ),
                'useCurrent': True,
                'collapse': False,
                # 'format': 'LTS',
            },
            attrs={
                'icon_toggle': True,
            }
        ),
    )
    duration_hours = forms.IntegerField(initial=1)
    duration_minutes = forms.IntegerField(initial=0)
    add_for_a_week = forms.BooleanField(required=False)

    def __init__(self, barbery, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.barbery = barbery

    def clean_start_time(self):
        cd = self.cleaned_data
        if cd['start_time'] < timezone.now():
            raise ValidationError(_('Entered time has passed.'))
        return cd['start_time']

    def clean(self):
        cd = self.cleaned_data
        self.cleaned_data['duration'] = timedelta(hours=cd['duration_hours'], minutes=cd['duration_minutes'])
        if cd.get('start_time', None) and \
                not TimeSlot.can_create_bulk(cd['start_time'], cd['duration'], cd['add_for_a_week'], self.barbery):
            raise ValidationError(_('This time slot collides with some of your previous slots.'))


class AddSlotsAdminForm(forms.ModelForm):
    add_for_a_week = forms.BooleanField(required=False)

    class Meta:
        model = TimeSlot
        fields = ['barbery', 'start_time', 'duration']

    def clean_start_time(self):
        cd = self.cleaned_data
        if cd['start_time'] < timezone.now():
            raise ValidationError(_('Entered time has passed.'))
        return cd['start_time']

    def clean(self):
        cd = self.cleaned_data
        if cd.get('start_time', None) and \
                not TimeSlot.can_create_bulk(cd['start_time'], cd['duration'], cd['add_for_a_week'], cd['barbery']):
            raise ValidationError(_('This time slot collides with some of your previous slots.'))

    def save(self, *args, **kwargs):
        cd = self.cleaned_data
        TimeSlot.create_bulk(start_time=cd['start_time'],
                             duration=cd['duration'],
                             add_for_a_week=cd['add_for_a_week'],
                             barbery=cd['barbery'])
        # todo: fix this bug

        kwargs.pop('commit', False)
        return super().save(commit=False, *args, **kwargs)


class BarberyUpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Barbery
        fields = ['name', 'email', 'address', ]

    def clean_email(self):
        user = User.objects.get(id=self.instance.id)
        prev_email = user.email
        try:
            if self.cleaned_data['email'] != prev_email:
                User.objects.get(email=self.cleaned_data['email'])
                raise ValidationError(_('Email "%(email)s" has been taken.')%{'email':self.cleaned_data['email']})
        except User.DoesNotExist:
            pass

        return self.cleaned_data['email']


class TimeSlotDeleteForm(forms.Form):
    slots = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, barbery, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slots'].queryset = barbery.time_slots.all()

    def save(self):
        slots = self.cleaned_data['slots']
        for slot in slots:
            if slot.reserved == False:
                slot.delete()
