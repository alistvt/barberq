from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
# Create your models here.


class Barbery(User):
    name = models.CharField(max_length=100, verbose_name=_('Barbery\'s name'))
    address = models.CharField(max_length=1000, unique=True, verbose_name=_('Address'))
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
