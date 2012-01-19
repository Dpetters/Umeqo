import threading

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.validators import email_re

def is_valid_email(email):
    return True if email_re.match(email) else False

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list, attachment_name=None, attachment_content=None, attachment_mimetype=None):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.attachment_name = attachment_name
        self.attachment_content = attachment_content
        self.attachment_mimetype = attachment_mimetype
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMessage(self.subject, self.html_content, settings.DEFAULT_FROM_EMAIL, self.recipient_list)
        if self.attachment_name and self.attachment_content and self.attachment_mimetype:
            msg.attach(self.attachment_name, self.attachment_content, self.attachment_mimetype)
        msg.content_subtype = "html"
        msg.send()

def send_html_mail(subject, html_content, recipient_list, attachment_name=None, attachment_content=None, attachment_mimetype=None):
    EmailThread(subject, html_content, recipient_list, attachment_name, attachment_content, attachment_mimetype).start()