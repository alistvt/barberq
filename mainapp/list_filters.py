from datetime import date

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# create custom filter classes for admin's site


class SpecialTimesFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('start time')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'time'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('morning', _('morning (06:00 - 10:00)')),
            ('noon', _('noon (10:00 - 14:00)')),
            ('afternoon', _('afternoon (14:00 - 18:00)')),
            ('night', _('night (18:00 - 24:00)')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'morning':
            return queryset.filter(start_time__hour__gte='06',
                                   start_time__hour__lt='10')
        if self.value() == 'noon':
            return queryset.filter(start_time__hour__gte='10',
                                   start_time__hour__lt='14')
        if self.value() == 'afternoon':
            return queryset.filter(start_time__hour__gte='14',
                                   start_time__hour__lt='18')
        if self.value() == 'night':
            return queryset.filter(start_time__hour__gte='18',
                                   start_time__hour__lt='24')


class FilterOption:
    def __init__(self, name, value, title, querydict):
        # name is the name of get variable and value is its value
        # title is the title that is shown it template
        self.title = title
        self.active = False
        self.querydict = self.create_querydict(name, value, querydict)
        self.url = self.generate_url()

    def create_querydict(self, name, value, querydict):
        querydict = dict(querydict)
        if name not in querydict:
            querydict[name] = [value]
            self.active = False
        else:
            if querydict[name][0] == value:
                self.active = True
            else:
                querydict[name][0] = value
                self.active = False
        return querydict

    def generate_url(self):
        url = '?'
        for name, value in self.querydict.items():
            url += name+'='+value[0]+'&'
        return url

    def __str__(self):
        return 'FilterOption(title={}, url={}'.format(self.title, self.url)

    def __repr__(self):
        return self.__str__()


class ReservationFilter:
    def __init__(self, querydict):
        self.name = 'reserved'
        # self.querydict = dict(querydict.iterlists())
        self.options = {
            'all': FilterOption(self.name, 'None', _('All'), querydict),
            'yes': FilterOption(self.name, '1', _('Yes'), querydict),
            'no': FilterOption(self.name, '0', _('No'), querydict),
        }

    def __str__(self):
        return 'ReservationFilter(options={}'.format(self.options)

