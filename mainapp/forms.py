from django import forms
from django.forms import ModelForm, ValidationError, Form
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

from mainapp.models import Reservation, Barbery


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
    password = forms.PasswordInput()
