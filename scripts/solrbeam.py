#!/usr/bin/python
import sys
import os
cwd = os.getcwd()
pd = os.path.pardir
solrdir = pd + r'/apache-solr-1.4.1'
if pd not in sys.path:
    sys.path.append(pd)
import urllib2
from time import strftime, gmtime
import settings

try:
    solrpanel = urllib2.urlopen(settings.HAYSTACK_SOLR_URL)
except urllib2.URLError:
    os.chdir(cwd)
    os.chdir(solrdir)
    os.system('nohup java -jar start.jar > ../logs/solr-reboots.log 2>&1 &')
    os.chdir(cwd)
    print 'Restarted solr on ' + strftime("%Y-%m-%d %H:%M:%S", gmtime())
else:
    print 'Everything is fine! on ' + strftime("%Y-%m-%d %H:%M:%S", gmtime())