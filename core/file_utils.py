import os
import re

def find_first_file(file_path, regex):
    files = os.listdir(file_path)
    regex = re.compile(regex)
    for f in files:
        if re.match(regex, f):
            return "%s%s" % (file_path, f)