from django.contrib import admin
from .models import Barbery, Reservation, TimeSlot, UserProfile
# Register your models here.


class BarberyAdmin(admin.ModelAdmin):
    #todo
    # Model Admins inherited from user model, should always exclude some fields, specially password (it's always excluded in our admins)
    # In order to create a better profile admin, take a look at django user admin, specially these two lines:
    # :
    # form = UserChangeForm
    # add_form = UserCreationForm

    exclude = ('password', )
    fields = ('name', ('first_name', 'last_name'), 'email', 'address', 'is_active', )
    list_display = ('name', 'first_name', 'last_name', 'address', 'is_active', )
    search_fields = ('name', 'first_name', 'last_name', 'address', )
    list_filter = ('is_active', )
    ordering = ('name', )


class UserProfileAdmin(admin.ModelAdmin):
    fields = ('email', ('first_name', 'last_name'), 'is_active', )
    list_display = ('email', 'first_name', 'last_name', 'is_active', )
    search_fields = ('email', 'first_name', 'last_name', )
    list_filter = ('is_active', )
    ordering = ('email',)


class TimeSlotAdmin(admin.ModelAdmin):
    exclude = ('created_date', )
    fields = ('barbery', ('start_time', 'duration'), )
    list_display = ('__str__', 'barbery', 'start_time', 'duration', 'reserved',)
    search_fields = ('barbery', )
    list_filter = ('reserved', )
    ordering = ('-start_time', )


class ReservationAdmin(admin.ModelAdmin):
    exclude = ('created_date', )
    fields = ('user', 'slot', )
    list_display = ('__str__', 'user', 'slot')
    # list_display = ('__str__', 'user', 'barbery', 'slot__start_time', 'slot__duration', )
    # should be written functions
    search_fields = ('user', 'slot__barbery', )
    ordering = ('-created_date', )


admin.site.register(Barbery, BarberyAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(TimeSlot, TimeSlotAdmin)
admin.site.register(Reservation, ReservationAdmin)
