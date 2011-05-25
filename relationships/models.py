from django.db import models

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from core.models import RelationshipType
from relationships.managers import RelationshipManager


class Relationship(models.Model):
    user = models.ForeignKey(User)
    type = models.ForeignKey(RelationshipType, related_name="relationships", default=1)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    objects = RelationshipManager()

    class Meta:
        verbose_name = _('relationship')
        verbose_name_plural = _('relationships')
        unique_together = (('user', 'content_type', 'object_id'),)
    
    def __unicode__(self):
        return "[%s] %s, %s" % (self.type.name, self.user.username, self.content_object)
