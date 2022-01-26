import os
import pathlib
import sqlite3
import sys
from shutil import copy2

import pandas as pd

allowed_file_types = [".txt", ".json", ".csv", ".db", ".sqlite"]
csv_types = [".txt", ".csv"]
sql_types = [".sqlite", ".db"]


# db and sqlite are both sqlite files, with different extensions
# as are csv and txt in this case


class ParsedFile:
    def __init__(self, file: pathlib.Path, df: pd.DataFrame):
        self.file = file
        self.df = df

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

    def create_skeleton(self):
        os.mkdir(self.base_path())
        os.mkdir(self.out_path())
        copy2(f.name, self.base_path())

    def meta_info(self) -> str:
        outputtypes = None
        if self.file.suffix in csv_types:
            outputtypes = [".json", ".sqlite"]
        elif self.file.suffix == ".json":
            outputtypes = [".csv", ".sqlite"]
        elif self.file.suffix in sql_types:
            outputtypes = [".json", ".csv"]

        return f"""Input Type: {self.file.suffix}
Output Types: {", ".join(outputtypes)}
Columns: {", ".join(list(self.df.columns))}
Rows: {len(self.df)}"""

    def convert_file(self):
        self.create_skeleton()
        if self.file.suffix not in csv_types:
            self.df.to_csv(self.csv())
        if self.file.suffix not in sql_types:
            conn = sqlite3.connect(self.sqlite())
            self.df.to_sql(self.file.stem, conn)
            conn.close()
        if self.file.suffix != ".json":
            self.df.to_json(self.json(), orient="index")

        with open(os.path.join(self.base_path(), "information.txt"), "w") as meta:
            meta.write(self.meta_info())


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

    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    conn.close()
    return df


def parse_file(file: pathlib.Path, *argv) -> ParsedFile:
    df = None
    if file.suffix in csv_types:
        df = pd.read_csv(file, sep=argv[0])
    elif file.suffix == ".json":
        df = pd.read_json(file)
    elif file.suffix in sql_types:
        df = parse_sqlite(file, argv[0])

    return ParsedFile(file, df)


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        path = input("Please specify the file you want to convert: ")
    else:
        path = args[1]

    if not os.path.isfile(path):
        print(f"{path} either does not exist or is not a file")
        exit(1)

    f = pathlib.Path(path)

    if f.suffix not in allowed_file_types:
        print(f"{f} cannot be converted")

    arg = None

    if f.suffix in csv_types:
        if len(args) < 3:
            arg = input("Please input the csv seperator: ")
        else:
            arg = args[2]

    if f.suffix in sql_types:
        if len(args) < 3:
            arg = input("Please input the table: ")
        else:
            arg = args[2]

    pf = parse_file(f, arg)
    pf.convert_file()
