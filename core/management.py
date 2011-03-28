"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs): #@UnusedVariable
        notification.create_notice_type("invitation_received", _("Event Invitation Received"), _("you have received an invitation to an event"))
        notification.create_notice_type("invitation_accepted", _("Event Invitation Acceptance Received"), _("an invitation you sent has been accepted"))

        notification.create_notice_type("new_student_matches", _("New Student Matches"), _("there are new students that match your default filtering parameters"))
                    
        notification.create_notice_type("new_deadline", _("New Deadline"), _("a company you're subscribed to has posted a new deadline"))
        notification.create_notice_type("new_event", _("New Event"), _("a company you're subscribed to has posted a new event"))
    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"