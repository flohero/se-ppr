import json
import os
import pathlib
import sqlite3

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
        self._out_path = "./"

    @property
    def out_path(self) -> str:
        """
        :return: the output directory in the base_path
        """
        return self._out_path

    @out_path.setter
    def out_path(self, out_path):
        self._out_path = out_path

    def csv(self) -> str:
        """
        :return: csv target file in the out_path
        """
        return os.path.join(self._out_path, self.file.stem + ".csv")

    def json(self) -> str:
        """
        :return: json target file in the out_path
        """
        return os.path.join(self._out_path, self.file.stem + json_type)

    def sqlite(self) -> str:
        """
        :return: sqlite target file in the out_path
        """
        return os.path.join(self._out_path, self.file.stem + ".sqlite")

    def convert_file(self, dest_type: str) -> str:
        """
        Converts the input file into all other available file types, excluding the input file type.
        The files are created in the out directory and meta information are written into a file in the target directory
        """
        if dest_type in csv_types:
            self.df.to_csv(self.csv(), index=False)
            return self.csv()
        elif dest_type in sql_types:
            conn = sqlite3.connect(self.sqlite())
            self.df.to_sql(self.file.stem, conn)
            conn.close()
            return self.sqlite()
        elif dest_type == json_type:
            self.df.to_json(self.json(), orient="records")
            return self.json()


def get_sqlite_table_name(connection: sqlite3.Connection) -> str:
    c = connection.cursor()
    c = c.execute(f"SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    if len(tables) == 0:
        connection.close()
        raise ValueError("No tables in sqlite file")

    if len(tables) > 1:
        connection.close()
        raise ValueError("Too many tables in sqlite file")

    return tables[0][0]


def parse_sqlite(file: pathlib.Path) -> pd.DataFrame:
    """
    Parses a sqlite database table into a pandas DataFrame
    :param file: sqlite database
    :return: pandas DataFrame
    """
    conn = sqlite3.connect(file)
    table = get_sqlite_table_name(conn)
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    conn.close()
    return df


def parse_file(file: pathlib.Path) -> ParsedFile:
    """
    Parses an input file of json, csv or sqlite type
    :param file: input file with json, csv, txt, sqlite or db extension
    :return: an instance of ParsedFile
    """
    if file.suffix in csv_types:
        df = pd.read_csv(file, sep=",")
    elif file.suffix == json_type:
        try:
            with open(file, "r") as json_file:
                json.load(json_file)
        except Exception:
            raise f"{file} does not contain valid json content"
        df = pd.read_json(file)
    elif file.suffix in sql_types:
        df = parse_sqlite(file)
    else:
        raise "Not a valid file type"

    return ParsedFile(file, df)


def convert_file(source: str, dest_path: str, dest_type: str) -> str:
    pf = parse_file(pathlib.Path(source))
    pf.out_path = dest_path
    return pathlib.Path(pf.convert_file(dest_type)).name


def file_allowed(filename: str) -> bool:
    return pathlib.Path(filename).suffix in allowed_file_types


def file_exists(filepath: str) -> bool:
    return pathlib.Path(filepath).exists()
