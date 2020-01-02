#!/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
from shutil import copyfile

def import_file(original_dir, file_root, filename, target_dir="./potytfonts", convert=None):
    file_to_import_fullpath = os.path.join(file_root, filename)
    target_path = os.path.join(target_dir, file_to_import_fullpath.replace("{}/".format(os.path.commonpath([file_to_import_fullpath, original_dir])), ""))
    print("Importing {} to {}...".format(file_to_import_fullpath, target_path))
    font_target_dir = os.path.dirname(target_path)
    os.makedirs(font_target_dir, exist_ok=True)
    copyfile(file_to_import_fullpath, target_path)
    if convert == "dfont":
        print("Converting {} with fondu...".format(target_path))
        subprocess.run(["fondu", os.path.abspath(target_path)], cwd=font_target_dir)
        # Clean all conversion files (.dont, .bdf).
        for filepath in os.listdir(font_target_dir):
            if filepath.endswith(".dfont") or filepath.endswith(".bdf"):
                os.remove(os.path.join(font_target_dir, filepath))
    

def convert_and_import_from_directory(target_dir):
    for file_root, _directories, files in os.walk(target_dir):
        for filename in files:
            if ".ttf" in filename:
                import_file(target_dir, file_root, filename)
            if ".dfont" in filename:
                import_file(target_dir, file_root, filename, convert="dfont")


if __name__ == '__main__':
    target_dir = sys.argv[1]
    convert_and_import_from_directory(target_dir)
