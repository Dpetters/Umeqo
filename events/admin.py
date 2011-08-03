from django.contrib import admin

from events.models import Event, EventType


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Required Info', {'fields': ['owner', 'name', 'slug', 'start_datetime', 'type', 'is_public']}),
        ('Extra Content', {'fields': ['edits', 'attending_employers', 'end_datetime', 'location', 'audience', 'description']}),
    ]
    list_display = ('name', 'owner', 'start_datetime', 'end_datetime', 'type', 'location', 'is_public')
    list_filter = ('owner', 'type', 'audience', 'is_public')
    search_fields = ['name', 'description']
    date_hierarchy = 'start_datetime'
admin.site.register(Event, EventAdmin)


class EventTypeAdmin(admin.ModelAdmin):
    fields = ['name']
    ordering = ('-last_updated',)
admin.site.register(EventType, EventTypeAdmin)
