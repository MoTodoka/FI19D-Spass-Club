from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from services.data import *
from services.data import _DataConverter, _DataRepository


@dataclass
class Player(Data):
    uid: int
    name: str
    birth_date: date

    def get_title(self) -> str:
        return "Spieler"

    def __str__(self):
        return self.name

    def get_service(self) -> PlayerService:
        return PlayerService()


class _PlayerConverter(_DataConverter):
    def get_data_from_dictionary(self, dictionary: dict) -> Player:
        return Player(int(dictionary["uid"]),
                      dictionary["name"],
                      datetime.strptime(dictionary["birth_date"], DATE_TIME_FORMAT))


class _PlayerRepository(_DataRepository):
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
    repository: _DataRepository.__class__ = _PlayerRepository

    def get_new(self) -> Player:
        return self.data(0,
                         "",
                         datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))

    def get_most_active(self, number: int):
        return self.repository().get_most_active(number)
