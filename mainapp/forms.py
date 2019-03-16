from datetime import date, datetime, timedelta
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

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        # if start_time < datetime.now():
        #     raise ValidationError(_('Entered time has passed.'))
        # todo : why does this give me error?!
        return self.cleaned_data['start_time']

    def clean(self):
        pass


class AddSlotsAdmin(forms.ModelForm):
    add_for_a_week = forms.BooleanField(required=False)

    class Meta:
        model = TimeSlot
        fields = ['barbery', 'start_time', 'duration']

    def clean_start_time(self):
        return self.cleaned_data['start_time']

    def clean(self):
        pass


class BarberyUpdateProfileForm(ModelForm):
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
