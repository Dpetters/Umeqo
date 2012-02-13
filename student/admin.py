from __future__ import division
from __future__ import absolute_import

from django.contrib import admin

from student.models import Student, StudentPreferences, StudentStatistics, StudentInvite, StudentDeactivation

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user', 'profile_created', 'date_created', 'last_updated')
    search_fields = ['first_name', 'last_name']
admin.site.register(Student, StudentAdmin)

class StudentInviteAdmin(admin.ModelAdmin):
    fields = ['code', 'used']
    list_display = ('code', 'used', 'last_updated')
    date_hierarchy = 'last_updated'
admin.site.register(StudentInvite, StudentInviteAdmin)

class StudentDeactivationAdmin(admin.ModelAdmin):
    fields = ['student', 'suggestion']
    list_display = ('student', 'suggestion', 'date_created')
    date_hierarchy = 'date_created'
admin.site.register(StudentDeactivation, StudentDeactivationAdmin)

class StudentPreferencesAdmin(admin.ModelAdmin):
    fields = ['email_on_invite_to_public_event', 'email_on_invite_to_private_event', 'email_on_new_subscribed_employer_event', 'receive_monthly_newsletter']
    list_display = ('student', 'last_updated', 'date_created')
    date_hierarchy = 'date_created'
admin.site.register(StudentPreferences, StudentPreferencesAdmin)

class StudentStatisticsAdmin(admin.ModelAdmin):
    fields = []
    list_display = ('student', 'last_updated', 'date_created')
    date_hierarchy = 'date_created'
admin.site.register(StudentStatistics, StudentStatisticsAdmin)
