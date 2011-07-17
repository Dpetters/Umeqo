from django.db import models

class StudentManager(models.Manager):
    use_for_related_fields = True
    
    def visible(self):
        return self.filter(user__is_active=True, user__userattributes__is_verified=True)