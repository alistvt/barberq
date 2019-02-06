from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

# Create your models here.
class Barbery(models.Model):
    barber = models.OneToOneField(User, related_name='barbery', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=1000, unique=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)

class TimeSlot(models.Model):
    barbery = models.ForeignKey(Barbery, related_name='timeslots', on_delete=models.CASCADE)
    createdDate = models.DateTimeField(auto_now_add=True)
    startTime = models.DateTimeField()
    duration = models.DurationField(default=timedelta(hours=1))
    reserved = models.BooleanField(default=False)
