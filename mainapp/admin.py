from django.contrib import admin
from .models import Barbery, UserProfile, TimeSlot, Reservation
# Register your models here.


class BarberyAdmin(admin.ModelAdmin):
    pass


class UserProfileAdmin(admin.ModelAdmin):
    pass


class TimeSlotAdmin(admin.ModelAdmin):
    pass


class ReservationAdmin(admin.ModelAdmin):
    pass
