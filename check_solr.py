#!/usr/bin/python
import os
import settings
import urllib2

from time import strftime, gmtime

solrdir = r'apache-solr-1.4.1'

try:
    solrpanel = urllib2.urlopen(settings.HAYSTACK_SOLR_URL)
except urllib2.URLError:
    os.chdir(solrdir)
    os.system('nohup java -jar start.jar > ../logs/solr-reboots.log 2>&1 &')
    print 'Restarted solr on ' + strftime("%Y-%m-%d %H:%M:%S", gmtime())
else:
    print 'Everything is fine! on ' + strftime("%Y-%m-%d %H:%M:%S", gmtime())