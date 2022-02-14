import os
import pathlib
import shutil
from os import listdir
from os.path import isfile

db_file = "./metadata.sqlite"
upload_dir = "./out"


def path_of_uploaded_file(filename: str):
    return os.path.join(upload_dir, filename)


def get_all_uploaded_files() -> list:
    return [f for f in listdir(upload_dir) if isfile(path_of_uploaded_file(f))]


def add_file(filepath: str):
    shutil.copyfile(filepath, os.path.join(upload_dir, pathlib.Path(filepath).name))


def remove_file(filename: str):
    target = path_of_uploaded_file(filename)
    os.remove(target)
