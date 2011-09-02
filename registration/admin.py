from django.contrib import admin
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from registration.models import RegistrationProfile, InterestedPerson, \
                                 UserAttributes, SessionKey, LoginAttempt, RegException

class LoginAttemptAdmin(admin.ModelAdmin):
    pass
admin.site.register(LoginAttempt, LoginAttemptAdmin)

class RegExceptionAdmin(admin.ModelAdmin):
    pass
admin.site.register(RegException, RegExceptionAdmin)

class InterestedPersonAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email', 'summer_plans', 'auto_email', 'final', 'emailed']
    list_display = ('first_name', 'last_name', 'email', 'auto_email', 'final', 'emailed')
admin.site.register(InterestedPerson, InterestedPersonAdmin)


class RegistrationProfileAdmin(admin.ModelAdmin):
    actions = ['activate_users', 'resend_activation_email']
    list_display = ('user', 'activation_key_expired')
    raw_id_fields = ['user']
    search_fields = ('user__username', 'user__first_name')

    def activate_users(self, request, queryset):
        """
        Activates the selected users, if they are not alrady
        activated.
        
        """
        for profile in queryset:
            RegistrationProfile.objects.activate_user(profile.activation_key)
    activate_users.short_description = _("Activate users")

    def resend_activation_email(self, request, queryset):
        """
        Re-sends activation emails for the selected users.

        Note that this will *only* send activation emails for users
        who are eligible to activate; emails will not be sent to users
        whose activation keys have expired or who have already
        activated.
        
        """
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        for profile in queryset:
            if not profile.activation_key_expired():
                profile.send_activation_email(site)
    resend_activation_email.short_description = _("Re-send activation emails")
admin.site.register(RegistrationProfile, RegistrationProfileAdmin)


class SessionKeyAdmin(admin.ModelAdmin):
    fields=[]
    list_display=['session_key', 'user', 'date_created']
    
admin.site.register(SessionKey, SessionKeyAdmin) 

    
class UserAttributesAdmin(admin.ModelAdmin):
    fields = ['user', 'is_verified']
    list_display=['user', 'is_verified']
admin.site.register(UserAttributes, UserAttributesAdmin)