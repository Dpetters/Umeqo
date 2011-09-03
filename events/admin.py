from django.contrib import admin

from events.models import Event, RSVP, Invitee, Attendee, DroppedResume
from core.models import EventType


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
    fields = ['name', 'sort_order']
    list_display = ('name', 'sort_order')
    ordering = ('-last_updated',)
admin.site.register(EventType, EventTypeAdmin)

class RSVPAdmin(admin.ModelAdmin):
    pass
admin.site.register(RSVP, RSVPAdmin)

class InviteeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Invitee, InviteeAdmin)

class AttendeeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Attendee, AttendeeAdmin)

class DroppedResumeAdmin(admin.ModelAdmin):
    pass
admin.site.register(DroppedResume, DroppedResumeAdmin)