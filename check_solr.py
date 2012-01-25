#!/usr/bin/python
import os
import settings
import urllib2

from core.email import send_html_mail
from time import strftime, gmtime

solrdir = r'apache-solr-1.4.1'
managers = [mail_tuple[1] for mail_tuple in settings.MANAGERS]
    
try:
    solrpanel = urllib2.urlopen(settings.HAYSTACK_SOLR_URL)
except urllib2.URLError:
    os.chdir(solrdir)
    os.system('nohup java -jar start.jar > ../logs/solr-reboots.log 2>&1 &')
    print 'Restarted solr on ' + strftime("%Y-%m-%d %H:%M:%S", gmtime())
    try:
        solrpanel = urllib2.urlopen(settings.HAYSTACK_SOLR_URL)
    except urllib2.URLError:
        send_html_mail("[Umeqo] Site #%s DOWN" % settings.SITE_ID, "Site #%s'w solr is down. You should probably check that shit out, bro.", managers)

else:
    print 'Everything is fine! on ' + strftime("%Y-%m-%d %H:%M:%S", gmtime())