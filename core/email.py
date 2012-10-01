import re
import threading

from BeautifulSoup import BeautifulSoup
from pynliner import Pynliner

from django.conf import settings as s
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.core.validators import email_re

def is_valid_email(email):
    return True if email_re.match(email) else False

def get_basic_email_context():
    context = {'current_site':Site.objects.get_current(),
               'STATIC_URL': s.STATIC_URL}
    if s.SITE_NAME == "Prod":
        context['protocol'] = "https"
    else:
        context['protocol'] = "http"
    return context


class EmailThread(threading.Thread):
    def __init__(self, subject, text_content, html_content, recipient_list, attachment_name=None, attachment_content=None, attachment_mimetype=None):
        self.subject = subject
        self.recipient_list = recipient_list
        self.text_content = text_content
        if html_content:
            print html_content
            self.html_content = Pynliner().from_string(html_content).run()
            print self.html_content
            soup = BeautifulSoup(self.html_content)
            hidden_tags = soup.findAll(lambda x: re.search("display: ?none", x['style']))
            if hidden_tags:
                for tag in hidden_tags:
                    tag.extract()
            self.html_content = str(soup)
        else:
            self.html_content = None
        self.attachment_name = attachment_name
        self.attachment_content = attachment_content
        self.attachment_mimetype = attachment_mimetype
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMultiAlternatives(self.subject, self.text_content, s.DEFAULT_FROM_EMAIL, self.recipient_list)
        if self.attachment_name and self.attachment_content and self.attachment_mimetype:
            msg.attach(self.attachment_name, self.attachment_content, self.attachment_mimetype)
        if self.html_content:
            msg.attach_alternative(self.html_content, "text/html")
        msg.send()

def send_email(subject, text_content, recipient_list, html_content=None, attachment_name=None, attachment_content=None, attachment_mimetype=None):
    EmailThread(subject, text_content, html_content, recipient_list, attachment_name, attachment_content, attachment_mimetype).start()    
