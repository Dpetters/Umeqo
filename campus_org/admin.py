from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _

from campus_org.models import CampusOrg


class CampusOrgAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Required Info', {'fields': ['name', 'type']}),
        ('Extra Info', {'fields': ['email', 'website', 'image', 'description', 'display']}),
    ]
    list_display = ('name', 'type', 'display')
    list_filter = ('type',)
    search_fields = ['name']
    date_hierarchy = 'last_updated'

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