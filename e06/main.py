import os
import pathlib
import sqlite3
import sys
from shutil import copy2

import pandas as pd

allowed_file_types = [".txt", ".json", ".csv", ".db", ".sqlite"]


# db and sqlite are both sqlite files, with different extensions
# as are csv and txt in this case


class ParsedFile:
    def __init__(self, file: pathlib.Path, df: pd.DataFrame):
        self.file = file
        self.df = df
        os.mkdir(self.base_path())
        os.mkdir(self.out_path())
        copy2(file.name, self.base_path())

    def base_path(self) -> str:
        return self.file.stem

    def out_path(self) -> str:
        return os.path.join(self.base_path(), "out")

    def csv(self):
        return os.path.join(self.out_path(), self.file.stem + ".csv")

    def json(self):
        return os.path.join(self.out_path(), self.file.stem + ".json")

    def sqlite(self):
        return os.path.join(self.out_path(), self.file.stem + ".sqlite")

    def convert_file(self):
        if self.file.suffix not in [".txt", ".csv"]:
            self.df.to_csv(self.csv())
        if self.file.suffix not in [".db", ".sqlite"]:
            conn = sqlite3.connect(self.sqlite())
            self.df.to_sql(self.file.stem, conn)
            conn.close()
        if self.file.suffix != ".json":
            self.df.to_json(self.json(), orient='index')


def parse_sqlite(file: pathlib.Path, table: str) -> pd.DataFrame:
    if not table:
        raise "Need a table name"
    conn = sqlite3.connect(file)
    cur = conn.cursor()
    # Find all tables of the sql database and check if table exists
    tables = cur.execute(
        "SELECT name FROM sqlite_master WHERE type=? and name = ?;", ("table", table)
    )
    if len(tables.fetchall()) != 1:
        conn.close()
        raise f"{table} not found in sqlite-file {file}"

    df = pd.read_sql_table(table, conn)
    conn.close()
    return df


def parse_file(file: pathlib.Path, *argv) -> ParsedFile:
    df = None
    if file.suffix in [".txt", ".csv"]:
        df = pd.read_csv(file, sep=argv[0])
    elif file.suffix == ".json":
        df = pd.read_json(file)
    elif file.suffix in [".db", ".sqlite"]:
        df = parse_sqlite(file, argv[0])

    return ParsedFile(file, df)


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print(
            "First argument filename, second argument optional a table name or csv seperator"
        )
    path = args[1]

    if not os.path.isfile(path):
        print(f"{path} either does not exist or is not a file")

    file = pathlib.Path(path)

    if file.suffix not in allowed_file_types:
        print(f"{file} cannot be converted")

    pf = None
    if len(args) == 3:
        pf = parse_file(file, *args[2::])
    else:
        pf = parse_file(file)

    pf.convert_file()
