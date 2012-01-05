from django.contrib import admin

from events.models import FeaturedEvent, Event, RSVP, Invitee, Attendee, DroppedResume
from core.models import EventType


class FeaturedEventAdmin(admin.ModelAdmin):
    pass
admin.site.register(FeaturedEvent, FeaturedEventAdmin)

class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Required Info', {'fields': ['owner', 'name', 'slug', 'short_slug', 'start_datetime', 'type', 'is_public', 'cancelled', 'archived']}),
        ('Extra Content', {'fields': ['edits', 'attending_employers', 'end_datetime', 'location', 'is_drop', 'latitude', 'longitude', 'audience', 'description']}),
    ]
    list_display = ('name', 'owner', 'start_datetime', 'end_datetime', 'type', 'location', 'is_drop', 'is_public', 'cancelled', 'archived')
    list_filter = ('owner', 'type', 'audience', 'is_public', 'is_drop')
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