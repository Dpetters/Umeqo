import os
import sys
import fnmatch
import subprocess

pattern = '*.png'
wd = os.path.pardir

for dirpath, dirnames, filenames in os.walk(wd):
    for filename in fnmatch.filter(filenames,pattern):
        subprocess.call("./pngout -y " +os.path.join(dirpath, filename), shell=True)