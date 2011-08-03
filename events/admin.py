from django.contrib import admin

from events.models import Event, EventType


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Required Info', {'fields': ['owner', 'name', 'slug', 'start_datetime', 'type']}),
        ('Extra Content', {'fields': ['end_datetime', 'location', 'audience', 'description']}),
    ]
    list_display = ('name', 'owner', 'start_datetime', 'end_datetime', 'type', 'location')
    list_filter = ('owner', 'type', 'audience')
    search_fields = ['name', 'description']
    date_hierarchy = 'start_datetime'
admin.site.register(Event, EventAdmin)


class EventTypeAdmin(admin.ModelAdmin):
    fields = ['name']
    ordering = ('-last_updated',)
admin.site.register(EventType, EventTypeAdmin)
