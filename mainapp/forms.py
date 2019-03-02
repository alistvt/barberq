from django.forms import ModelForm
from mainapp.models import Reservation


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['user', 'slot', ]
