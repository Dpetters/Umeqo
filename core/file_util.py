import os


def findFile(file_path, extension):
    files = os.listdir(file_path)
    for f in files:
        file_extension = f.split(".")[-1]
        if file_extension == file_extension:
            print f