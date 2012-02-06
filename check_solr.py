#!/usr/bin/python
import sys
import time
import os
import settings as s
import urllib2

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from core.email import send_html_mail
from time import strftime, gmtime

solrdir = s.ROOT + '/apache-solr-3.5.0/example'
managers = [mail_tuple[1] for mail_tuple in s.MANAGERS]

for i in range(10):
    try:
        solrpanel = urllib2.urlopen(s.HAYSTACK_SOLR_URL)
        sys.exit(0)
    except urllib2.URLError:
        print 'solr request fail'
        time.sleep(2)

try:
    solrpanel = urllib2.urlopen(s.HAYSTACK_SOLR_URL)
except urllib2.URLError:
    try:
        os.chdir(solrdir)
        if s.SITE_NAME == "Demo":
            os.system('nohup java -Djetty.port="8984" -jar start.jar > ../../logs/solr-reboots.log 2>&1 &')
        else:
            os.system('nohup java -jar start.jar > ../../logs/solr-reboots.log 2>&1 &')
    except Exception as e:
        print e
    else:
        os.chdir(s.ROOT)
        time.sleep(10)
        os.system('python manage.py update_index')
        print 'Restarted solr on ' + strftime("%Y-%m-%d %H:%M:%S", gmtime())
else:
    time.sleep(5)
    try:
        solrpanel = urllib2.urlopen(s.HAYSTACK_SOLR_URL)
    except urllib2.URLError:
        send_html_mail("[Umeqo] %s's SOLR DOWN" % s.SITE_NAME, "%s's solr is down. You should probably check that shit out, bro." % s.SITE_NAME, managers)
    print "%s's solr is running fine! on %s" % (s.SITE_NAME, strftime('%Y-%m-%d %H:%M:%S'), gmtime())