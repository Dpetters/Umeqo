"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.db import models
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from help import enums

class Topic(models.Model):
    """
    Generic Topics for FAQ question grouping
    """
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    sort_order = models.IntegerField(_('sort order'), default=0, help_text='The order you would like the topic to be displayed.')
    audience = models.IntegerField(choices = enums.TOPIC_AUDIENCE_CHOICES)
    
    class Meta:
        ordering = ['sort_order', 'name']

    def __unicode__(self):
        return self.name


class Question(models.Model):
    """
    Represents a frequently asked question.
    """
    topic = models.ForeignKey(Topic)    
    status = models.IntegerField( choices=enums.QUESTION_STATUS_CHOICES, help_text="Only questions with their status set to 'Active' will be displayed." )
    audience = models.IntegerField(choices = enums.TOPIC_AUDIENCE_CHOICES, default=enums.ALL)
    sort_order = models.IntegerField(_('sort order'), default=0, help_text='This in which you would like the question to be displayed.')
    
    question = models.TextField(_('question'), unique=True)
    answer = models.TextField( _('answer')) 
    
    slug = models.SlugField( max_length=100, help_text="This is a unique identifier that allows your questions to display its detail view, ex 'how-can-i-contribute'", )

    created_by = models.ForeignKey(User, null=True, editable=False, related_name="%(class)s_created" )    
    created_on = models.DateTimeField( _('created on'), default=datetime.now, editable=False)
    updated_on = models.DateTimeField( _('updated on'), editable=False)
    updated_by = models.ForeignKey(User, null=True, editable=False, related_name="%(class)s_updated" )
    
    class Meta:
        ordering = ['sort_order', 'created_on']

    def __unicode__(self):
        return self.question

    def save(self, *args, **kwargs):
        self.updated_on = datetime.now()
        super(Question, self).save(*args, **kwargs)