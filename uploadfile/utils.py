import os


def getfilename(title):
    return os.path.splitext(title)[0]


def getfilesize(size):
    if size < 1024:
        size = str(round(size, 1)) + 'KB'
    elif size/1024 < 1024:
        size = str(round(size/1024, 1)) + 'MB'
    else:
        size = str(round(size/1024/1024, 1)) + 'GB'
    return size
