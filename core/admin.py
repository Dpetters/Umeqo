from __future__ import division
from __future__ import absolute_import

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _

from core.models import Tutorial, CampusOrgType, Course, Language, SchoolYear, GraduationYear, Industry, Topic, Question, EmploymentType, Location

class TutorialAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    
    def response_change(self, request, obj):
        """
        Determines the HttpResponse for the change_view stage.
        """
        if request.POST.has_key("_viewnext"):
            msg = (_('The %(name)s "%(obj)s" was changed successfully.') %
                   {'name': force_unicode(obj._meta.verbose_name),
                    'obj': force_unicode(obj)})
            all_tutorials = list(obj.__class__.objects.all())
            next = all_tutorials[all_tutorials.index(obj)+1:]
            if next:
                self.message_user(request, msg)
                return HttpResponseRedirect("../%s/" % next[0].pk)
        return super(TutorialAdmin, self).response_change(request, obj)

admin.site.register(Tutorial, TutorialAdmin)


class LocationAdmin(admin.ModelAdmin):
    fields = ['name', 'display_name', 'building_num', 'latitude', 'longitude', 'keywords', 'image_url']
    list_display = ('name', 'display_name', 'building_num', 'latitude', 'longitude', 'image_url')
    search_fields = ['keywords', 'name']

admin.site.register(Location, LocationAdmin)

    
class TopicAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug':('name',)}
    list_display = ('name', 'sort_order')
    search_fields = ['name']
    
admin.site.register(Topic, TopicAdmin)


class QuestionAdmin(admin.ModelAdmin):
    fields= ['audience', 'sort_order', 'topic', 'question', 'answer', 'slug', 'display']
    prepopulated_fields = {'slug':('question',)}
    list_display = ['question', 'topic', 'audience', 'sort_order', 'click_count', 'display']
    list_filter = ['topic', 'audience', 'display']
    search_fields = ['question', 'answer']
    
    def save_model(self, request, obj, form, change):
        # Overridden because I want to also set who created this instance.
        instance = form.save( commit=False )
        if instance.id is None:
            instance.created_by = request.user
                
        instance.updated_by = request.user
        instance.save()
        return instance

admin.site.register(Question, QuestionAdmin)


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'last_login', 'date_joined')
    list_filter = ('groups','is_active', 'is_staff')
    search_fields = ['first_name', 'last_name', 'email']
    date_hierarchy = 'date_joined'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class IndustryAdmin(admin.ModelAdmin):
    fields = ['name']
    search_fields = ['name']

admin.site.register(Industry, IndustryAdmin)


class SchoolYearAdmin(admin.ModelAdmin):
    fields = ['name', 'name_plural']
    ordering = ('-last_updated',)

admin.site.register(SchoolYear, SchoolYearAdmin)


class GraduationYearAdmin(admin.ModelAdmin):
    fields = ['year']
    ordering = ('-year',)

admin.site.register(GraduationYear, GraduationYearAdmin)


class LanguageAdmin(admin.ModelAdmin):
    fields = ['name']
    ordering = ('-last_updated',)
    search_fields = ['name']

admin.site.register(Language, LanguageAdmin)


class CampusOrgTypeAdmin(admin.ModelAdmin):
    fields = ['name']
    ordering = ('-last_updated',)
    date_hierarchy = 'last_updated'

admin.site.register(CampusOrgType, CampusOrgTypeAdmin)


class EmploymentTypeAdmin(admin.ModelAdmin):
    fields = ['name', 'sort_order']
    ordering = ('-last_updated',)
    date_hierarchy = 'last_updated'

admin.site.register(EmploymentType, EmploymentTypeAdmin)


class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Required Info', {'fields': ['name', 'num', 'sort_order']}),
        ('Extra Content', {'fields': ['admin', 'ou', 'email', 'website', 'image', 'description', 'display']}),
    ]
    list_display = ('name', 'num', 'display', 'sort_order')
    search_fields = ['name']
    
    def response_change(self, request, obj):
        """
        Determines the HttpResponse for the change_view stage.
        """
        if request.POST.has_key("_viewnext"):
            msg = (_('The %(name)s "%(obj)s" was changed successfully.') %
                   {'name': force_unicode(obj._meta.verbose_name),
                    'obj': force_unicode(obj)})
            next = obj.__class__.objects.filter(id__gt=obj.id).order_by('name')[:1]
            if next:
                self.message_user(request, msg)
                return HttpResponseRedirect("../%s/" % next[0].pk)
        return super(CourseAdmin, self).response_change(request, obj)

admin.site.register(Course, CourseAdmin)