#!/usr/bin/env python
import zipfile
import os, sys
import datetime

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception('Robot name cannot be empty')
    folder_name = "/data/logs"
    zip_name = sys.argv[1] + "_logs_" + str(datetime.datetime.now()).replace(" ", "")

    if len(os.listdir(folder_name)) is 0:
        print("No files in directory")
        sys.exit()

    with zipfile.ZipFile(os.path.join(folder_name, zip_name) + '.zip', 'w') as zf:
        for item in os.listdir(folder_name):
            if item.endswith(".zip"):
                continue

            if os.path.isfile(os.path.join(folder_name, item)):
                zf.write(os.path.join(folder_name, item), item)
            else:
                for file in os.listdir(os.path.join(folder_name, item)):
                    zf.write(os.path.join(folder_name, item, file), os.path.join(item, file))
    
    for item in os.listdir(folder_name):
        if item.endswith(".zip"):
            continue
        if os.path.isfile(os.path.join(folder_name, item)):
            os.remove(os.path.join(folder_name, item))
        if os.path.isdir(os.path.join(folder_name, item)):
            for file in os.listdir(os.path.join(folder_name, item)):
                if os.path.isfile(os.path.join(folder_name, item, file)):
                    os.remove(os.path.join(folder_name, item, file))
            os.rmdir(os.path.join(folder_name, item))