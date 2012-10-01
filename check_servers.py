import datetime
import urllib2
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.conf import settings
from django.template import Context, loader
from django.template.loader import render_to_string

from core.email import get_basic_email_context, send_email


#manager list
managers = [mail_tuple[1] for mail_tuple in settings.MANAGERS]

# url definitions
prod_url = "https://www.umeqo.com/"
staging_url = "http://www.staging.umeqo.com/"
demo_url = "http://www.demo.umeqo.com/"
urls = [("PROD", prod_url), ("STAGING", staging_url), ("DEMO", demo_url)]

# staging auth setup
username = 'root'
password = 'C4pt4inCol4'

passwdmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
passwdmgr.add_password(None, staging_url, username, password)

authhandler = urllib2.HTTPBasicAuthHandler(passwdmgr)
opener = urllib2.build_opener(authhandler)
urllib2.install_opener(opener)

for server_type, url in urls:
    start = datetime.datetime.now()
    try:
        print url
        urllib2.urlopen(url)
    except urllib2.HTTPError as resp:
        if (resp != None and resp.code != 200):
            context = Context({'server_type':server_type, 'response_code':resp.code})
            context.update(get_basic_email_context())
            
            subject = ''.join(render_to_string('email_admin_subject.txt', {
                'message': "%s DOWN" % server_type
            }, context).splitlines())
            
            text_email_template_name='server_down.txt'
            text_email_body_template = loader.get_template(text_email_template_name)
            text_email_body = text_email_body_template.render(context)
            
            send_email(subject, text_email_body, managers)
    else:
        print "%s is up. Time taken to check: %s" % (server_type, datetime.datetime.now() - start)