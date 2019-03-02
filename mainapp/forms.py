from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _

from mainapp.models import Reservation


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['user', 'slot', ]

    def clean_slot(self):
        slot = self.cleaned_data['slot']
        if slot.reserved:
            raise ValidationError(_('This slot is reserved.'))
