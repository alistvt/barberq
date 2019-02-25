from django.contrib import admin
from .models import Barbery, UserProfile, TimeSlot, Reservation
# Register your models here.

class BarberyAdmin(admin.ModelAdmin):
    # Model Admins inherited from user model, should always exclude some fields, specially password (it's always excluded in our admins)
    # In order to create a better profile admin, take a look at django user admin, specially these two lines:

    # form = UserChangeForm
    # add_form = UserCreationForm

    # Take a look at django admin form documentation
    exclude = ('password',)
    fields = ('name', ('first_name', 'last_name'), 'email', 'address', 'is_active',)
    list_display = ('name', 'first_name', 'last_name', 'address', 'is_active', )
    search_fields = ('name', 'first_name', 'last_name', 'address',)
    #todo fix
    # We user list filter for fields with enumerated values, with less than around 10 choices. (e.g. gender).
    # Date or Time fields are not good for list filter. Use date_hierarchy instead
    list_filter = ('is_active', )
    ordering = ('name',)


class UserProfileAdmin(admin.ModelAdmin):
    pass


class TimeSlotAdmin(admin.ModelAdmin):
    pass


class ReservationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Barbery, BarberyAdmin)
