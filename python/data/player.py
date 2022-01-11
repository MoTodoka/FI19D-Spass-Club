from __future__ import annotations

from dataclasses import dataclass

from python.services.database_connection_service import *

from python.data.generic_data import Data, DataService, _DataConverter, _DataDbConnection


@dataclass
class Player(Data):
    uid: int
    name: str

    def get_title(self) -> str:
        return "Spieler"

    def __str__(self):
        return self.name

    def get_service(self) -> PlayerService:
        return PlayerService()


class _PlayerConverter(_DataConverter):
    def get_data_from_dictionary(self, dictionary: dict) -> Player:
        return Player(int(dictionary["uid"]),
                      dictionary["name"])


class _PlayerDbConnection(_DataDbConnection):
    table_name = "player"

    def get_most_active(self, number: int) -> [(Player, int)]:
        cur = self.con.sqlite3_con.cursor()
        cur.execute(
            '''SELECT p.*, COUNT(score.uid) AS scores FROM score 
            LEFT JOIN player p on p.uid = score.player GROUP BY p.uid LIMIT ?;''', (number,))
        rows: [sqlite3.Row] = cur.fetchall()
        result_set: [Player, int] = []
        for row in rows:
            result_set.append((_PlayerConverter().get_data_from_dictionary(row), row["scores"]))
        return result_set


class PlayerService(DataService):
    data: Data.__class__ = Player
    converter: _DataConverter.__class__ = _PlayerConverter
    repository: _DataDbConnection.__class__ = _PlayerDbConnection

    def get_new(self) -> Player:
        return self.data(0,
                         "")

    def get_most_active(self, number: int):
        return self.repository().get_most_active(number)
