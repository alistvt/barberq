from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Barbery(User):
    name = models.CharField(max_length=100, verbose_name=_('Barbery\'s name'))
    address = models.CharField(max_length=1000, unique=True, verbose_name=_('Address'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, blank=True, verbose_name=_('Slug for url'))

    def __str__(self):
        return '{name}'.format(name=self.name)

    # todo fix
    # Always write the class Meta for all of your models, and put these three items in it
    class Meta:
        verbose_name = _("Barbery")
        verbose_name_plural = _("Barberies")
        ordering = ['created_date']


class UserProfile(User):
    pass

    def __str__(self):
        return '{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name)


class TimeSlot(models.Model):
    barbery = models.ForeignKey(Barbery, related_name='time_slots', on_delete=models.CASCADE)

    # All of you models should contain the 'verbose_name' parameter: Translated and Capital
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    start_time = models.DateTimeField(verbose_name=_('Start time'))
    duration = models.DurationField(default=timedelta(hours=1), verbose_name=_('Duration'))
    reserved = models.BooleanField(default=False, verbose_name=_('Is reserved'))

    def __str__(self):
        return '{barbery}@{date}'.format(barbery=self.barbery, date=self.start_time)


class Reservation(models.Model):
    user = models.ForeignKey(UserProfile, related_name='reservations', on_delete=models.CASCADE)
    slot = models.OneToOneField(TimeSlot, related_name='reservation', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))

    def __str__(self):
        return '{user}-{slot}'.format(user=self.user, slot=self.slot)
