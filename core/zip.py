import zipfile
import os

def create_zip(path, relname, archname):
    archive = zipfile.ZipFile(archname, "w", zipfile.ZIP_DEFLATED)
    if os.path.isdir(path):
        zip_folder(path, relname, archive)
    else:
        archive.write(path, relname)
    archive.close()

def zip_folder(path, relname, archive):
    paths = os.listdir(path)
    for p in paths:
        p1 = os.path.join(path, p)
        p2 = os.path.join(relname, p)
        if os.path.isdir(p1): 
            zip_folder(p1, p2, archive)
        else:
            archive.write(p1, p2) 