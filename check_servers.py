import datetime
import urllib2
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.conf import settings
from core.email import send_html_mail


#manager list
managers = [mail_tuple[1] for mail_tuple in settings.MANAGERS]

# url definitions
prod_url = "http://www.umeqo.com/"
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

fine = True

while 1:

    for type, url in urls:
        try:
            urllib2.urlopen(url)
            # if no error now and there was an error previously, send email to all managers to say that the server is back up
            if (!fine):
                send_html_mail("[Umeqo] %s UP" % type, "%s is back up at %s. You should probably just chill, bro." % (type, resp.code, str(datetime.datetime.now())), managers)
                fine = True
        except urllib2.HTTPError as resp:
            if (resp != None):
                # if error, send email to all managers to say that the server is down with an error code
                if (resp.code != 200):
                    send_html_mail("[Umeqo] %s DOWN" % type, "%s is down with error message %s at %s. You should probably check that shit out, bro." % (type, resp.code, str(datetime.datetime.now())), managers)
                    fine = False
                # if no error now and there was an error previously, send email to all managers to say that the server is back up
                elif (!fine):
                    send_html_mail("[Umeqo] %s UP" % type, "%s is back up at %s. You should probably just chill, bro." % (type, resp.code, str(datetime.datetime.now())), managers)
                    fine = True
