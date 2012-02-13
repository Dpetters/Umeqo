import time
from datetime import datetime

from django.conf import settings as s
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.template import Context, loader

from core.email import send_html_mail
from events.models import Event
from student.models import Student

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        events =  Event.objects.filter(include_in_monthly_newsletter=True)
        print events
        if events.exists():
            month = datetime.now().strftime("%B")
            t = loader.get_template("monthly_newsletter.html")
            for i, student in enumerate(Student.objects.filter(user__is_active=True, user__userattributes__is_verified=True, studentpreferences__receive_monthly_newsletter=True, first_name="Dmitrij")):
                if i % 5 == 0:
                    time.sleep(1)
                context = {
                'student':student,
                'events':events,
                'month':month,
                'current_site': Site.objects.get(id=s.SITE_ID)
                }
                body = t.render(Context(context))
                f = open("monthly_email.html", "w")
                f.write(body)
                f.close()
                #send_html_mail("[Umeqo] %s Newsletter" % month, body, [student.user.email])
        #for event in events:
        #    event.include_in_monthly_newsletter = False
        #    event.save()