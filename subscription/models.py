import datetime
import utils

from django.conf import settings as s
from django.db import models

from core.texttime import stringify

class Transaction(models.Model):
    employer = models.ForeignKey("employer.Employer", null=True)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    person = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    amount = models.FloatField(null=True)
    comment = models.TextField()
    payment = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-timestamp',)
        
    def save(self):
        if self.payment:
            if self.payment > 0:
                self.payment = True

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
    uid = models.PositiveIntegerField(unique=True, null=True)
    name = models.CharField(max_length=100, unique=True, null=False)
    description = models.TextField(blank=True)
    price = models.FloatField()
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
        return "%s Subscription" % self.name.title()

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

class Card(models.Model):
    employer = models.ForeignKey("employer.Employer")
    last_4_digits = models.CharField(max_length=4)
    expiration_date = models.DateField(default=datetime.date.today)


class EmployerSubscription(models.Model):
    employer = models.OneToOneField("employer.Employer")
    subscription = models.ForeignKey(Subscription)
    expires = models.DateField(null = True, default=datetime.date.today)
    cancelled = models.BooleanField(default=False)

    grace_timedelta = datetime.timedelta(getattr(s, 'SUBSCRIPTION_GRACE_PERIOD', 2))

    def premium_subscription(self):
        try:
            premium_subscription = Subscription.objects.get(uid=s.PREMIUM_SUBSCRIPTION_UID)
        except:
            return False
        else:
            return self.subscription == premium_subscription
        
    def time_left(self):
        return stringify(self.expires + self.grace_timedelta - datetime.date.today())
    
    def in_grace_period(self):
        over = datetime.date.today() - self.expires
        return over > datetime.timedelta() and over < self.grace_timedelta
    
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