from django.contrib import admin

from employer.models import Employer, EmployerStatistics, ResumeBook, Recruiter, RecruiterStatistics, RecruiterPreferences


class ResumeBookAdmin(admin.ModelAdmin):
    fields = ['resume_book', 'name']
    list_display = ['recruiter', 'name', 'date_created']
    
admin.site.register(ResumeBook, ResumeBookAdmin)


class RecruiterAdmin(admin.ModelAdmin):
    fields = ['user', 'employer']
    list_display = ('user', 'employer', 'last_updated', 'date_created')
    search_fields = ['employer']
    date_hierarchy = 'date_created'
        
admin.site.register(Recruiter, RecruiterAdmin)


class RecruiterStatisticsAdmin(admin.ModelAdmin):
    fields = []
    list_display = ('recruiter', 'last_updated', 'date_created')
    search_fields = ['recruiter']
    date_hierarchy = 'date_created'
        
admin.site.register(RecruiterStatistics, RecruiterStatisticsAdmin)


class RecruiterPreferencesAdmin(admin.ModelAdmin):
    fields = ['email_on_rsvp', 'results_per_page', 'default_student_ordering']
    list_display = ('recruiter', 'last_updated', 'date_created')
    search_fields = ['recruiter']
    date_hierarchy = 'date_created'
        
admin.site.register(RecruiterPreferences, RecruiterPreferencesAdmin)
    
    
class EmployerAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'slug', 'industries', 'main_contact', 'main_contact_phone']
    list_display = ('name', 'main_contact', 'main_contact_phone', 'date_created')
    search_fields = ['name', 'industries__name', 'main_contact']
    date_hierarchy = 'date_created'
    
admin.site.register(Employer, EmployerAdmin)


class EmployerStatisticsAdmin(admin.ModelAdmin):
    fields = []
    list_display = ('employer', 'last_updated', 'date_created')
    search_fields = ['employer']
    date_hierarchy = 'date_created'
            
admin.site.register(EmployerStatistics, EmployerStatisticsAdmin)