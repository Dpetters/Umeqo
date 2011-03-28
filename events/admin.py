"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.contrib import admin
from events.models import Event, EventType

class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Required Info', {'fields': ['employer', 'name', 'datetime', 'type']}),
        ('Extra Content', {'fields': ['days', 'hours', 'minutes', 'location', 'audience', 'description']}),
    ]
    list_display = ('employer', 'name', 'datetime', 'type', 'days', 'hours', 'minutes', 'location')
    list_filter = ('employer', 'type', 'audience')
    search_fields = ['name', 'description']
    date_hierarchy = 'datetime'
    
class EventTypeAdmin(admin.ModelAdmin):
    fields = ['name']
    ordering = ('-last_updated',)

admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)