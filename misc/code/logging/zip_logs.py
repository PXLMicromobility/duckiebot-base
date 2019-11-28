#!/usr/bin/env python
import os, sys
import zipfile

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(file))

if __name__ == '__main__':
    if len(sys.argv) is 1:
        raise Exception("The source directory is required!")
    src = sys.argv[1]
    dest = sys.argv[2]
    zipf = zipfile.ZipFile(dest + '.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(src, zipf)
    zipf.close()
