#!/usr/bin/python
import sys
import time
import os
import settings as s
import urllib2

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from core.email import send_email
from time import strftime, gmtime

solrdir = s.ROOT + '/apache-solr-3.5.0/example'
managers = [mail_tuple[1] for mail_tuple in s.MANAGERS]

print "checking on %s's solr on %s" % (s.SITE_NAME, strftime('%Y-%m-%d %H:%M:%S', gmtime()))

for i in range(10):
    try:
        solrpanel = urllib2.urlopen(s.HAYSTACK_SOLR_URL)
        print "%s's solr is up and running on %s" % (s.SITE_NAME, strftime('%Y-%m-%d %H:%M:%S', gmtime()))
        sys.exit(0)
    except urllib2.URLError:
        print "%s's solr request fail on %s" % (s.SITE_NAME, strftime('%Y-%m-%d %H:%M:%S', gmtime()))
        time.sleep(2)

print "going to restart %s's solr" % s.SITE_NAME

try:
    os.chdir(solrdir)
    if s.SITE_NAME == "Demo":
        os.system('nohup java -Djetty.port="8984" -jar start.jar > ../../logs/solr-reboots.log 2>&1 &')
    else:
        os.system('nohup java -jar start.jar > ../../logs/solr-reboots.log 2>&1 &')
except Exception as e:
    print e
else:
    time.sleep(10)
    try:
        solrpanel = urllib2.urlopen(s.HAYSTACK_SOLR_URL)
    except urllib2.URLError:
        send_email("[Umeqo Admin] %s's SOLR DOWN" % s.SITE_NAME, "%s's solr is down and couldn't be restarted automatically. You should probably check that shit out, bro." % s.SITE_NAME, managers)
        print "was not able to restart  %s's solr on %s and emailed admins" % (s.SITE_NAME, strftime('%Y-%m-%d %H:%M:%S', gmtime()))
    else:
        print "successfully finished restarting  %s's solr on %s" % (s.SITE_NAME, strftime('%Y-%m-%d %H:%M:%S', gmtime()))
        os.system('python manage.py update_index')

