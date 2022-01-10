from __future__ import annotations

import os
import sqlite3
from sqlite3 import Error

from werkzeug.exceptions import ServiceUnavailable, Conflict


class Connection:
    """
    Die Verbindung zur Datenbank.
    """
    sqlite3_con: sqlite3.Connection = None
    db_path: str

    def __init__(self, db_path: str = 'SQLite/spass_club.db'):
        self.db_path = db_path
        self.connect_to_db()

    def connect_to_db(self):
        try:
            self.sqlite3_con = sqlite3.connect(self.db_path)
            self.sqlite3_con.row_factory = sqlite3.Row
        except Error as e:
            raise ServiceUnavailable(str(e))

    def __del__(self):
        self.sqlite3_con.close()

    def remove_db(self):
        self.sqlite3_con.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def create_tables(self, sql_file: str = "SQLite/tables.sql"):
        cur = self.sqlite3_con.cursor()
        sql_file = open(sql_file)
        sql_as_string = sql_file.read()
        cur.executescript(sql_as_string)

    def reset_database(self):
        try:
            self.remove_db()
            self.connect_to_db()
            self.create_tables()
        except PermissionError:
            raise Conflict()

    def load_test_data(self, sql_file: str = "SQLite/test_data.sql"):
        cur = self.sqlite3_con.cursor()
        sql_file = open(sql_file, "rb")
        sql_as_string = sql_file.read().decode("UTF-8")
        cur.executescript(sql_as_string)
