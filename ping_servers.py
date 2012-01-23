import urllib2
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.conf import settings
from core.email import send_html_mail



#manager list
managers = [mail_tuple[1] for mail_tuple in settings.MANAGERS]


# url definitions
base_url = "http://www.umeqo.com"
staging_url = "http://www.staging.umeqo.com"
demo_url = "http://www.demo.umeqo.com"


# begin - staging auth setup

username = 'root'
password = 'Bulle1tN3at'

passwdmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
passwdmgr.add_password(None, staging_url, username, password)

authhandler = urllib2.HTTPBasicAuthHandler(passwdmgr)
opener = urllib2.build_opener(authhandler)
urllib2.install_opener(opener)

# end - staging auth setup


try:
    urllib2.urlopen(base_url)
except urllib2.HTTPError as resp:
    # if error, send email to all managers with error code
    if (resp != None and resp.code != 200):
        send_html_mail("UMEQO.COM DOWN","The production server www.umeqo.com is down with error message {}. You should probably check that shit out, bro".format(resp.code),managers)

try:
    urllib2.urlopen(demo_url)
except urllib2.HTTPError as resp:
    # if error, send email to all managers with error code
    if (resp != None and resp.code != 200):
        send_html_mail("DEMO.UMEQO.COM DOWN","The demo server www.demo.umeqo.com is down with error message {}. You should probably check that shit out, bro".format(resp.code),managers)

try:
    urllib2.urlopen(staging_url)
except urllib2.HTTPError as resp:
    # if error, send email to all managers with error code
    if (resp != None and resp.code != 200):
        send_html_mail("STAGING.UMEQO.COM DOWN","The staging server www.staging.umeqo.com is down with error message {}. You should probably check that shit out, bro".format(resp.code),managers)
