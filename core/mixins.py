import datetime
from django.db import models


class DateTracking(models.Model):
    last_updated = models.DateTimeField(editable=False, auto_now=True, default=datetime.datetime.now())
    date_created = models.DateTimeField(editable=False, auto_now_add=True, default=datetime.datetime.now())

    class Meta:
        abstract = True

class DateCreatedTracking(models.Model):
    date_created = models.DateTimeField(editable=False, auto_now_add=True, default=datetime.datetime.now())

    class Meta:
        abstract = True