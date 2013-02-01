import time

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.utils.html import strip_tags

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        f = open("announce_acquisition.txt", "w")
        recipients = ['dmitrij@umeqo.com', "dpetters91@gmail.com"]
        html_content = render_to_string("umeqo-readyforce.html", {})
        text_content = strip_tags(html_content)
        for recipient in recipients:
            msg = EmailMultiAlternatives('[Umeqo] Umeqo + Readyforce', text_content, 'Umeqo Team <team@umeqo.com>', [recipient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            f.write("%s\n" % recipient)
            time.sleep(30)
        f.close()
