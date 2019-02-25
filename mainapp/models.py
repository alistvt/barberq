from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Barbery(User):
    name = models.CharField(max_length=100, verbose_name='barbery\'s name')
    address = models.CharField(max_length=1000, unique=True, verbose_name='address')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='creation date')
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, blank=True, verbose_name='slug for url')

    def __str__(self):
        return '{name}'.format(name=self.name)


class UserProfile(User):
    pass

    def __str__(self):
        return '{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name)


class TimeSlot(models.Model):
    barbery = models.ForeignKey(Barbery, related_name='time_slots', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='creation date')
    start_time = models.DateTimeField(verbose_name='start time')
    duration = models.DurationField(default=timedelta(hours=1), verbose_name='duration')
    reserved = models.BooleanField(default=False, verbose_name='is reserved')

    def __str__(self):
        return '{barbery}@{date}'.format(barbery=self.barbery, date=self.start_time)


class Reservation(models.Model):
    user = models.ForeignKey(UserProfile, related_name='reservations', on_delete=models.CASCADE)
    slot = models.OneToOneField(TimeSlot, related_name='reservation', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='creation date')

    def __str__(self):
        return '{user}-{slot}'.format(user=self.user, slot=self.slot)
