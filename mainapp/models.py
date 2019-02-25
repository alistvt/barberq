from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Barbery(User):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=1000, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, blank=True)


class UserProfile(User):
    pass


class TimeSlot(models.Model):
    barbery = models.ForeignKey(Barbery, related_name='time_slots', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    duration = models.DurationField(default=timedelta(hours=1))
    reserved = models.BooleanField(default=False)


class Reservation(models.Model):
    user = models.ForeignKey(UserProfile, related_name='reservations', on_delete=models.CASCADE)
    slot = models.OneToOneField(TimeSlot, related_name='reservation', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
