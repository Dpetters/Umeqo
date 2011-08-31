from django.db import models

class EmployerManager(models.Manager):
    def visible(self):
        return self.filter(visible=True)