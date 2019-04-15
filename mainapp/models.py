from datetime import timedelta, date, datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
# Create your models here.


class Barbery(User):
    name = models.CharField(max_length=100, verbose_name=_('Barbery\'s name'))
    address = models.CharField(max_length=1000, verbose_name=_('Address'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, blank=True, verbose_name=_('Slug for url'))

    def __str__(self):
        return '{name}'.format(name=self.name)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.name
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)

        super(Barbery, self).save(*args, **kwargs)

    def has_free_time(self, start_time, duration):
        today_slots = self.time_slots.filter(start_time__date=start_time.date())
        for slot in today_slots:
            if (slot.start_time + slot.duration > start_time and slot.start_time <= start_time) or \
               (slot.start_time + slot.duration >= start_time + duration and slot.start_time < start_time + duration):
                return False
        return True

    def num_of_reservations(self):
        return self.time_slots.filter(reserved=True).count()

    def num_of_time_slots(self):
        return self.time_slots.all().count()

    num_of_reservations.short_description = _('Reservations')
    num_of_time_slots.short_description = _('Time Slots')

    class Meta:
        verbose_name = _("Barbery")
        verbose_name_plural = _("Barberies")
        ordering = ['name']


class UserProfile(User):
    pass

    class Meta:
        verbose_name = _("User profile")
        verbose_name_plural = _("User profiles")
        ordering = ['username']

    def __str__(self):
        return '{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        super(UserProfile, self).save(*args, **kwargs)


class TimeSlot(models.Model):
    # TODO: why I can't add verbose name here and what should I do???
    barbery = models.ForeignKey(Barbery, related_name='time_slots', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    start_time = models.DateTimeField(verbose_name=_('Start time'))
    duration = models.DurationField(default=timedelta(hours=1), verbose_name=_('Duration'))
    reserved = models.BooleanField(default=False, verbose_name=_('Is reserved'))

    class Meta:
        verbose_name = _("Time slot")
        verbose_name_plural = _("Time slots")
        ordering = ['-start_time']

    def __str__(self):
        return '{barbery}@{date}'.format(barbery=self.barbery, date=self.start_time)

    @staticmethod
    def create_single(start_time, duration, barbery):
        if barbery.has_free_time(start_time, duration):
            time_slot = TimeSlot(start_time=start_time, duration=duration, barbery=barbery)
            time_slot.save()
            return time_slot
        else:
            pass

    @staticmethod
    def check_create_single(start_time, duration, barbery):
        if barbery.has_free_time(start_time, duration):
            return True
        else:
            return False

    @staticmethod
    def can_create_bulk(start_time, duration, add_for_a_week, barbery):
        if add_for_a_week:
            for i in range(7):
                if not TimeSlot.check_create_single(start_time+timedelta(days=i), duration, barbery):
                    return False
            return True
        else:
            return TimeSlot.check_create_single(start_time, duration, barbery)

    @staticmethod
    def create_bulk(start_time, duration, add_for_a_week, barbery):
        if add_for_a_week:
            for i in range(7):
                time_slot = TimeSlot.create_single(start_time+timedelta(days=i), duration, barbery)
        else:
            time_slot = TimeSlot.create_single(start_time, duration, barbery)
        return time_slot

    @staticmethod
    def search_for_barbery(barbery, search_context):
        # slots = barbery.time_slots.filter()
        pass


class Reservation(models.Model):
    user = models.ForeignKey(UserProfile, related_name='reservations', on_delete=models.CASCADE)
    slot = models.OneToOneField(TimeSlot, related_name='reservation', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")
        ordering = ['slot']

    def __str__(self):
        return '{user}-{slot}'.format(user=self.user, slot=self.slot)

    def save(self, *args, **kwargs):
        self.slot.reserved = True
        self.slot.save()
        super(Reservation, self).save(*args, **kwargs)
