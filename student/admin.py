from django.contrib import admin

from student.models import Student, StudentPreferences, StudentStatistics

class StudentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Student, StudentAdmin)

class StudentPreferencesAdmin(admin.ModelAdmin):
    fields = ['email_on_invite_to_public_event', 'email_on_invite_to_private_event', 'email_on_new_event']
    list_display = ('student', 'last_updated', 'date_created')
    date_hierarchy = 'date_created'
admin.site.register(StudentPreferences, StudentPreferencesAdmin)

class StudentStatisticsAdmin(admin.ModelAdmin):
    fields = []
    list_display = ('student', 'last_updated', 'date_created')
    date_hierarchy = 'date_created'
admin.site.register(StudentStatistics, StudentStatisticsAdmin)
