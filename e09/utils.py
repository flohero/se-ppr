import json
import os
import sqlite3
from os import listdir
from os.path import isfile

from flask import redirect, url_for

db_file = "./metadata.sqlite"
upload_dir = "./out"


def create_error_page(error_msg: str):
    return redirect(
        url_for(
            "error",
            error=error_msg
        )
    )


def file_does_not_exist_error():
    return create_error_page(f"File does not exist")


def path_of_uploaded_file(filename: str):
    return os.path.join(upload_dir, filename)


def get_all_uploaded_files() -> list:
    return [
        f
        for f in listdir(upload_dir)
        if isfile(path_of_uploaded_file(f))
    ]


def remove_file(filename: str):
    target = path_of_uploaded_file(filename)
    os.remove(target)
    delete_entry(filename)


def create_database():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metadata (
        title text,
        url text,
        languages text,
        repository_count decimal,
        member_count decimal)
    """)
    conn.commit()
    conn.close()


def delete_entry(title):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM METADATA WHERE title LIKE ?", [title])
    conn.commit()
    conn.close()


def create_entry(title, url=None, languages=None, repository_count=None, member_count=None):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO metadata (title, url, languages, repository_count, member_count) VALUES(?,?,?,?,?)",
                   [title, url, languages, repository_count, member_count])
    conn.commit()
    conn.close()


def create_github_entry(data: dict):
    create_entry(data["title"] + ".json", data["url"], ", ".join(data["languages"]), data["repository_count"],
                 data["member_count"])
    with open(os.path.join(upload_dir, f"{data['title']}.json"), "w") as file:
        json.dump(data["repositories"], file)


def get_metadata(filename: str):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    d = cursor.execute("SELECT * FROM metadata WHERE title LIKE ?", [filename]).fetchone()
    conn.commit()
    conn.close()
    return d
