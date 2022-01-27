import csv
import json
import os
import pathlib
import sqlite3
import sys
from shutil import copy2

import pandas as pd

# Grouped csv and sqlite types
# db and sqlite are both sqlite files, with different extensions
# as are csv and txt in this case
csv_types = [".txt", ".csv"]
sql_types = [".sqlite", ".db"]

json_type = ".json"

# All allowed file types/extensions
allowed_file_types = [json_type, *csv_types, *sql_types]


class ParsedFile:
    """
    Represents a parsed file, containing a path to the original file and the pandas DataFrame
    """
    def __init__(self, file: pathlib.Path, df: pd.DataFrame):
        self.file = file
        self.df = df

    def base_path(self) -> str:
        """
        :return: the base path of the target directory
        """
        return self.file.stem

    def out_path(self) -> str:
        """
        :return: the output directory in the base_path
        """
        return os.path.join(self.base_path(), "out")

    def csv(self) -> str:
        """
        :return: csv target file in the out_path
        """
        return os.path.join(self.out_path(), self.file.stem + ".csv")

    def json(self) -> str:
        """
        :return: json target file in the out_path
        """
        return os.path.join(self.out_path(), self.file.stem + json_type)

    def sqlite(self) -> str:
        """
        :return: sqlite target file in the out_path
        """
        return os.path.join(self.out_path(), self.file.stem + ".sqlite")

    def create_skeleton(self) -> None:
        """
        Creates the target and out directories and copies the original file into the target directory
        """
        os.mkdir(self.base_path())
        os.mkdir(self.out_path())
        copy2(f.name, self.base_path())

    def meta_info(self) -> str:
        """
        Builds the meta information as a string.
        The string contains the input file type, the output type, the columns of the DataFrame and the rows of the DataFrame
        :return: the meta information as a string
        """
        outputtypes = None
        if self.file.suffix in csv_types:
            outputtypes = [json_type, ".sqlite"]
        elif self.file.suffix == json_type:
            outputtypes = [".csv", ".sqlite"]
        elif self.file.suffix in sql_types:
            outputtypes = [json_type, ".csv"]

        return f"""Input Type: {self.file.suffix}
Output Types: {", ".join(outputtypes)}
Columns: {", ".join(list(self.df.columns))}
Rows: {len(self.df)}"""

    def convert_file(self) -> None:
        """
        Converts the input file into all other available file types, excluding the input file type.
        The files are created in the out directory and meta information are written into a file in the target directory
        """
        self.create_skeleton()
        if self.file.suffix not in csv_types:
            self.df.to_csv(self.csv(), index=False)
        if self.file.suffix not in sql_types:
            conn = sqlite3.connect(self.sqlite())
            self.df.to_sql(self.file.stem, conn)
            conn.close()
        if self.file.suffix != json_type:
            self.df.to_json(self.json(), orient="records")

        with open(os.path.join(self.base_path(), "information.txt"), "w") as meta:
            meta.write(self.meta_info())


def parse_sqlite(file: pathlib.Path, table: str) -> pd.DataFrame:
    """
    Parses a sqlite database table into a pandas DataFrame
    :param file: sqlite database
    :param table: table in the sqlite database
    :return: pandas DataFrame
    """
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
    """
    Parses an input file of json, csv or sqlite type
    :param file: input file with json, csv, txt, sqlite or db extension
    :param argv: additional arguments for sqlite types it must contain the table name, for csv it must contain the seperator
    :return: an instance of ParsedFile
    """
    if file.suffix in csv_types:
        df = pd.read_csv(file, sep=argv[0])
    elif file.suffix == json_type:
        try:
            with open(file, "r") as json_file:
                json.load(json_file)
        except Exception:
            raise f"{file} does not contain valid json content"
        df = pd.read_json(file)
    elif file.suffix in sql_types:
        df = parse_sqlite(file, argv[0])
    else:
        raise "Not a valid file type"

    return ParsedFile(file, df)


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        path = input("Please specify the file you want to convert: ")
        if path == "":
            print("Input cant be empty")
            exit(1)
    else:
        path = args[1]

    if not os.path.isfile(path):
        print(f"{path} either does not exist or is not a file")
        exit(1)

    f = pathlib.Path(path)

    if f.suffix not in allowed_file_types:
        print(f"{f} cannot be converted")
        exit(1)

    arg = None

    if f.suffix in csv_types:
        if len(args) < 3:
            arg = input("Please input the csv seperator: ")
            if arg == "":
                print("Input cant be empty")
                exit(1)
        else:
            arg = args[2]

    if f.suffix in sql_types:
        if len(args) < 3:
            arg = input("Please input the table: ")
            if arg == "":
                print("Input cant be empty")
                exit(1)
        else:
            arg = args[2]

    pf = parse_file(f, arg)
    pf.convert_file()
