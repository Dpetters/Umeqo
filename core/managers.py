from django.db import models

class ActiveManager(models.Manager):
    def get_query_set(self):
        return super(ActiveManager, self).get_query_set().filter(is_active=True)
    def active(self):
        return self.filter(is_active=True)

class VisibleManager(models.Manager):
    def visible(self):
        return self.filter(display=True)