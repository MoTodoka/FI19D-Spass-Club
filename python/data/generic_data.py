from __future__ import annotations

import sqlite3
from abc import abstractmethod
from datetime import datetime

from python.services.database_connection_service import Connection

DATE_TIME_FORMAT: str = "%Y-%m-%dT%H:%M"


class Data:
    """
    Parent-Klasse für alle Daten-Klassen.\n
    Alle Daten-Klassen müssen das Attribut int(uid) enthalten.
    """
    uid: int

    @abstractmethod
    def get_title(self) -> str:
        pass

    @abstractmethod
    def __str__(self):
        pass

    def __lt__(self, other):
        return self.uid < other.uid

    @abstractmethod
    def get_service(self) -> DataService:
        pass


class _DataConverter:
    """
    Parent-Klasse für Daten-Konverter.\n
    Ermöglicht Objekte aus Dictionaries zu erzeugen.
    """

    @staticmethod
    def get_date_time_from(date_time_str: str) -> datetime:
        return datetime.strptime(date_time_str, DATE_TIME_FORMAT)

    @abstractmethod
    def get_data_from_dictionary(self, dictionary: dict) -> Data:
        pass

    def get_data_from_dictionaries(self, dictionaries: [dict]) -> []:
        result_set = []
        for row in dictionaries:
            result_set.append(self.get_data_from_dictionary(row))
        return result_set


class _DataDbConnection:
    """
    Implementiert Basis-Funktionalität für SQL-Abfragen.\n
    Rückgabewerte bei SELECTs sind sqlite3.Rows.
    """
    con: Connection = None
    table_name: str

    def __init__(self):
        self.con = Connection()
        self.con.sqlite3_con.cursor().execute("PRAGMA foreign_keys = ON;")

    def get_all(self) -> [sqlite3.Row]:
        cur = self.con.sqlite3_con.cursor()
        sql = f"SELECT * FROM {self.table_name};"
        cur.execute(sql)
        return cur.fetchall()

    def get_by_uid(self, uid: int) -> sqlite3.Row:
        cur = self.con.sqlite3_con.cursor()
        sql = f"SELECT * FROM {self.table_name} WHERE uid = ?;"
        cur.execute(sql, (uid,))
        return cur.fetchone()

    def update(self, dictionary: dict):
        cur = self.con.sqlite3_con.cursor()
        keys_values_list: [str] = []
        for key, value in dictionary.items():
            if key != "uid" and key != "service":
                if isinstance(value, Data):
                    keys_values_list.append(f"{key}={str(value.uid)}")
                elif isinstance(value, datetime):
                    keys_values_list.append(f"{key}=\"{datetime.strftime(value, DATE_TIME_FORMAT)}\"")
                else:
                    keys_values_list.append(f"{key}=\"{value}\"")
        key_values_str = ",".join(keys_values_list)
        sql = f"UPDATE {self.table_name} SET {key_values_str} WHERE uid = {dictionary.get('uid')}"
        cur.execute(sql)
        self.con.sqlite3_con.commit()

    def insert(self, dictionary: dict):
        cur = self.con.sqlite3_con.cursor()
        keys = ",".join([f"{key}"
                         for key, value in dictionary.items()
                         if key != "uid"
                         and key != "service"])
        values_list: [str] = []
        for key, value in dictionary.items():
            if key != "uid" and key != "service":
                if isinstance(value, Data):
                    values_list.append(str(value.uid))
                elif isinstance(value, datetime):
                    values_list.append(f"\"{datetime.strftime(value, DATE_TIME_FORMAT)}\"")
                else:
                    values_list.append(f"\"{value}\"")
        values_str = ",".join(values_list)
        sql = f"INSERT INTO {self.table_name} ({keys}) VALUES ({values_str})"
        cur.execute(sql)
        self.con.sqlite3_con.commit()

    def delete(self, uid: int) -> int:
        cur = self.con.sqlite3_con.cursor()
        sql = f"DELETE FROM {self.table_name} WHERE uid = ?"
        cur.execute(sql, (uid,))
        self.con.sqlite3_con.commit()
        return cur.rowcount


class DataService:
    """
    Parent-Klasse für Daten-Operationen.\n
    Diese Klasse für das Lesen und schreiben von Daten nutzen.
    """
    data: Data.__class__
    converter: _DataConverter.__class__
    repository: _DataDbConnection.__class__

    def get_all(self) -> [data]:
        rows: [sqlite3.Row] = self.repository().get_all()
        return self.converter().get_data_from_dictionaries(rows)

    def get_by_uid(self, uid: int) -> data:
        row: sqlite3.Row = self.repository().get_by_uid(uid)
        return self.converter().get_data_from_dictionary(row)

    def write(self, data: data):
        self.repository().write(data)

    def get_max(self) -> [data]:
        rows: [sqlite3.Row] = self.repository().get_all()
        result_set = self.converter().get_data_from_dictionaries(rows)
        result_set.sort(reverse=True)
        return result_set[0]

    @abstractmethod
    def get_new(self) -> Data:
        pass

    def delete(self, uid):
        return self.repository().delete(uid)

    def insert(self, data: Data):
        self.repository().insert(data.__dict__)

    def update(self, data: data):
        self.repository().update(data.__dict__)