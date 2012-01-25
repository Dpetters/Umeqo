#!/usr/bin/python
import os
solrdir = r'apache-solr-1.4.1'

import urllib2
from time import strftime, gmtime
import settings

try:
    solrpanel = urllib2.urlopen(settings.HAYSTACK_SOLR_URL)
except urllib2.URLError:
    os.chdir(solrdir)
    os.system('nohup java -jar start.jar > ../logs/solr-reboots.log 2>&1 &')
    print 'Restarted solr on ' + strftime("%Y-%m-%d %H:%M:%S", gmtime())
else:
    print 'Everything is fine! on ' + strftime("%Y-%m-%d %H:%M:%S", gmtime())