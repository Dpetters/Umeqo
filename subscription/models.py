import datetime
import utils

from django.conf import settings
from django.db import models
from django.contrib import auth

class Transaction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    subscription = models.ForeignKey('subscription.Subscription', null=True, blank=True, editable=False)
    user = models.ForeignKey(auth.models.User, null=True, blank=True, editable=False)
    amount = models.DecimalField(max_digits=64, decimal_places=2, null=True, blank=True, editable=False)
    comment = models.TextField(blank=True, default='')

    class Meta:
        ordering = ('-timestamp',)

_recurrence_unit_days = {
    'D' : 1.,
    'W' : 7.,
    'M' : 30.4368,                      # http://en.wikipedia.org/wiki/Month#Julian_and_Gregorian_calendars
    'Y' : 365.2425,                     # http://en.wikipedia.org/wiki/Year#Calendar_year
    }

_TIME_UNIT_CHOICES=(
    ('D', 'Day'),
    ('W', 'Week'),
    ('M', 'Month'),
    ('Y', 'Year'),
)

class Subscription(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=64, decimal_places=2)
    trial_period = models.PositiveIntegerField(null=True, blank=True)
    trial_unit = models.CharField(max_length=1, null=True, choices = (("", "No trial"),) + _TIME_UNIT_CHOICES)
    recurrence_period = models.PositiveIntegerField(null=True, blank=True)
    recurrence_unit = models.CharField(max_length=1, null=True, choices = (("", "No recurrence"),) + _TIME_UNIT_CHOICES)

    _PLURAL_UNITS = {
        'D': 'days',
        'W': 'weeks',
        'M': 'months',
        'Y': 'years',
    }

    class Meta:
        ordering = ('price','-recurrence_period')

    def __unicode__(self):
        return self.name

    def price_per_day(self):
        """Return estimate subscription price per day, as a float.

        This is used to charge difference when user changes
        subscription.  Price returned is an estimate; month length
        used is 30.4368 days, year length is 365.2425 days (averages
        including leap years).  One-time payments return 0.
        """
        if self.recurrence_unit is None:
            return 0
        return float(self.price) / (self.recurrence_period*_recurrence_unit_days[self.recurrence_unit])


class EmployerSubscription(models.Model):
    employer = models.OneToOneField("employer.Employer")
    subscription = models.OneToOneField(Subscription)
    expires = models.DateField(null = True, default=datetime.date.today)
    cancelled = models.BooleanField(default=False)

    grace_timedelta = datetime.timedelta(getattr(settings, 'SUBSCRIPTION_GRACE_PERIOD', 2))

    def expired(self):
        """Returns true if there is more than SUBSCRIPTION_GRACE_PERIOD
        days after expiration date."""
        return self.expires is not None and (
            self.expires + self.grace_timedelta < datetime.date.today() )
    expired.boolean = True

    def extend(self, timedelta=None):
        """Extend subscription by `timedelta' or by subscription's
        recurrence period."""
        if timedelta is not None:
            self.expires += timedelta
        else:
            if self.subscription.recurrence_unit:
                self.expires = utils.extend_date_by(
                    self.expires,
                    self.subscription.recurrence_period,
                    self.subscription.recurrence_unit)
            else:
                self.expires = None

    def __unicode__(self):
        rv = u"%s's %s" % ( self.employer, self.subscription )
        if self.expired():
            rv += u' (expired)'
        return rv