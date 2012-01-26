#!/usr/bin/python
import time
import os
import settings
import urllib2

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from core.email import send_html_mail
from time import strftime, gmtime

solrdir = r'apache-solr-1.4.1'
managers = [mail_tuple[1] for mail_tuple in settings.MANAGERS]
    
try:
    solrpanel = urllib2.urlopen(settings.HAYSTACK_SOLR_URL)
except urllib2.URLError:
    os.chdir(solrdir)
    # Demo needs a special port
    if settings.SITE_ID == 4:
        os.system('nohup java -Djetty.port="8984" -jar start.jar > ../logs/solr-reboots.log 2>&1 &')        
    else:
        os.system('nohup java -jar start.jar > ../logs/solr-reboots.log 2>&1 &')
    print 'Restarted solr on ' + strftime("%Y-%m-%d %H:%M:%S", gmtime())
    time.sleep(2)
    try:
        solrpanel = urllib2.urlopen(settings.HAYSTACK_SOLR_URL)
    except urllib2.URLError:
        send_html_mail("[Umeqo] Site #%s DOWN" % settings.SITE_ID, "Site #%s'w solr is down. You should probably check that shit out, bro." % settings.SITE_ID, managers)

else:
    print 'Everything is fine! on ' + strftime("%Y-%m-%d %H:%M:%S", gmtime())