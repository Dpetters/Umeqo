from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from django import forms

from core.view_helpers import employer_campus_org_slug_exists
from campus_org.models import CampusOrg

class CampusOrgAdminForm(forms.ModelForm):
    class Meta:
        model = CampusOrg
        
    def clean_slug(self):
        if self.cleaned_data['slug']:
            if employer_campus_org_slug_exists(self.cleaned_data['slug'], campusorg=self.instance):
                raise forms.ValidationError("A campus organization or employer with the slug %s already exists" % (self.cleaned_data['slug']))
        return self.cleaned_data['slug']

class CampusOrgAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Required Info', {'fields': ['name', 'type', 'school']}),
        ('Extra Info', {'fields': ['user', 'slug', 'email', 'website', 'image', 'description', 'display']}),
    ]
    list_display = ('name', 'school', 'type', 'display', 'user')
    list_filter = ('school', 'type')
    search_fields = ['name', 'school__name', 'user__username']
    date_hierarchy = 'last_updated'
    form = CampusOrgAdminForm
    
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
        return super(CampusOrgAdmin, self).response_change(request, obj)

admin.site.register(CampusOrg, CampusOrgAdmin)
