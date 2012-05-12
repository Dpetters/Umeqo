import os

from django.conf import settings as s

ckeditor_upload_path = "%s/media/ckeditor" % s.ROOT
if not os.path.exists(ckeditor_upload_path):
    os.makedirs(ckeditor_upload_path)