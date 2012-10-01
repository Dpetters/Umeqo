import os
import time

from datetime import datetime
from pynliner import Pynliner

from django.conf import settings as s
from django.core.management.base import BaseCommand
from django.template import Context
from django.template.loader import render_to_string

from core.email import get_basic_email_context, send_email
from events.models import Event
from student.models import Student


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        #employers = Employer.objects.visible().filter(feature_in_monthly_newsletter=True)
        all_events_and_deadlines = Event.objects.filter(include_in_monthly_newsletter=True)
        events = filter(lambda x: not x.is_deadline() and not x.is_past(), all_events_and_deadlines)
        deadlines = filter(lambda x: x.is_deadline(), all_events_and_deadlines)

        if events or deadlines:
            year = datetime.now().strftime("%Y")
            month = datetime.now().strftime("%B")

            for i, student in enumerate(Student.objects.filter(user__is_active=True, user__userattributes__is_verified=True, studentpreferences__receive_monthly_newsletter=True, first_name="Dmitrij")):
                
                if i % 5 == 0:
                    time.sleep(1)
                context = Context({
                'first_name':student.first_name,
                'student':student,
                #'employer':employers,
                'events':events,
                'deadlines':deadlines,
                'month':month,
                'year':year
                })
                context.update(get_basic_email_context())
                
                text_email_body = render_to_string("monthly_newsletter.txt", context)
                html_email_body = render_to_string("monthly_newsletter.html", context)
                html_email_body = Pynliner().from_string(html_email_body).run()

                subject = ''.join(render_to_string('email_subject.txt', {
                    'message': "%s Newsletter" % month
                }, context).splitlines())
                
                send_email(subject, text_email_body, [student.user.email])

            newsletter_path = "%s/newsletter/templates/%s/" % (s.ROOT, year)
            if not os.path.exists(newsletter_path):
                os.makedirs(newsletter_path)
            
            context['first_name'] = None
            context['student'] = None
            body = render_to_string("monthly_newsletter.html", context)
            body = Pynliner().from_string(body).run()
                                
            f = open("%s%s.html" % (newsletter_path, month), "w")
            f.write(body)
            f.close()
                
        #for event in events:
        #    event.include_in_monthly_newsletter = False
        #    event.save()
