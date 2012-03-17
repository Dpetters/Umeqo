from django.contrib import admin
from django.db import models
from django import forms

from ckeditor.widgets import CKEditorWidget
from employer.models import Employer, EmployerStatistics, ResumeBook, Recruiter, RecruiterStatistics, RecruiterPreferences
from core.view_helpers import employer_campus_org_slug_exists

class ResumeBookAdmin(admin.ModelAdmin):
    fields = ['resume_book', 'name', 'delivered']
    list_display = ['recruiter', 'name', 'delivered', 'date_created']
    
admin.site.register(ResumeBook, ResumeBookAdmin)


class RecruiterAdmin(admin.ModelAdmin):
    fields = ['user', 'employer']
    list_display = ('user', 'employer', 'last_updated', 'date_created')
    search_fields = ['employer__name']
    date_hierarchy = 'date_created'
        
admin.site.register(Recruiter, RecruiterAdmin)


class RecruiterStatisticsAdmin(admin.ModelAdmin):
    fields = []
    list_display = ('recruiter', 'last_updated', 'date_created')
    search_fields = ['recruiter__user__email']
    date_hierarchy = 'date_created'
        
admin.site.register(RecruiterStatistics, RecruiterStatisticsAdmin)


class RecruiterPreferencesAdmin(admin.ModelAdmin):
    fields = ['email_on_rsvp_to_public_event','email_on_rsvp_to_private_event', 'default_student_results_per_page', 'default_student_result_ordering']
    list_display = ('recruiter', 'last_updated', 'date_created')
    search_fields = ['recruiter__user__email']
    date_hierarchy = 'date_created'
        
admin.site.register(RecruiterPreferences, RecruiterPreferencesAdmin)


class EmployerAdminForm(forms.ModelForm):
    class Meta:
        model = Employer
        
    def clean_slug(self):
        if self.cleaned_data['slug']:
            if employer_campus_org_slug_exists(self.cleaned_data['slug'], employer=self.instance):
                raise forms.ValidationError("A campus organization or employer with the slug %s already exists" % (self.cleaned_data['slug']))
        return self.cleaned_data['slug']


class EmployerAdmin(admin.ModelAdmin):
    fields = ['name', 'logo', 'description', 'slug', 'offered_job_types', 'industries', 'careers_website', 'main_contact', 'main_contact_phone', 'main_contact_email', 'visible']
    list_display = ('name', 'main_contact', 'main_contact_phone', 'visible', 'date_created')
    search_fields = ['name', 'industries__name', 'main_contact']
    date_hierarchy = 'date_created'
    formfield_overrides = { models.TextField: {'widget': CKEditorWidget(attrs={'class':'ckeditor'})},}
    form = EmployerAdminForm
admin.site.register(Employer, EmployerAdmin)


class EmployerStatisticsAdmin(admin.ModelAdmin):
    fields = []
    list_display = ('employer', 'last_updated', 'date_created')
    search_fields = ['employer__name']
    date_hierarchy = 'date_created'
admin.site.register(EmployerStatistics, EmployerStatisticsAdmin)