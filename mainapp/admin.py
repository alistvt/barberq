from django.contrib import admin
from .models import Barbery, UserProfile, TimeSlot, Reservation
# Register your models here.


class BarberyAdmin(admin.ModelAdmin):
    list_display = ('name', 'first_name', 'last_name', 'address',)
    search_fields = ('name', 'first_name', 'last_name', 'address',)
    list_filter = ('created_date',)
    ordering = ('name',)


class UserProfileAdmin(admin.ModelAdmin):
    pass


class TimeSlotAdmin(admin.ModelAdmin):
    pass


class ReservationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Barbery, BarberyAdmin)
