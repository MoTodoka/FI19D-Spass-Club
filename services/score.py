from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from services.match import Match, MatchService
from services.player import Player, PlayerService
from services.data import Data, DataService, _DataConverter, _DataRepository, DATE_TIME_FORMAT


@dataclass
class Score(Data):
    uid: int
    match: Match
    player: Player
    timestamp: datetime
    score: Optional[int]

    def get_title(self) -> str:
        return "Ergebnis"

    def __str__(self):
        return f"{self.timestamp} - {self.player}: {self.score}"

    def __lt__(self, other):
        return self.score < other.score

    def get_service(self) -> ScoreService:
        return ScoreService()


class _ScoreConverter(_DataConverter):
    def get_data_from_dictionary(self, dictionary: dict) -> Score:
        return Score(int(dictionary["uid"]),
                     MatchService().get_by_uid(dictionary["match"]),
                     PlayerService().get_by_uid(dictionary["player"]),
                     datetime.strptime(dictionary["timestamp"], DATE_TIME_FORMAT),
                     int(dictionary["score"]))


class _ScoreRepository(_DataRepository):
    table_name = "score"

    def get_multiple_by_match(self, match_uid: int) -> [sqlite3.Row]:
        cur = self.con.sqlite3_con.cursor()
        cur.execute('''SELECT * FROM score WHERE match = ?;''', (str(match_uid),))
        return cur.fetchall()

    def get_multiple_by_player(self, player_uid: int) -> [sqlite3.Row]:
        cur = self.con.sqlite3_con.cursor()
        cur.execute('''SELECT * FROM score WHERE player = ?;''', (str(player_uid),))
        return cur.fetchall()


class ScoreService(DataService):
    data: Data.__class__ = Score
    converter: _DataConverter.__class__ = _ScoreConverter
    repository: _DataRepository.__class__ = _ScoreRepository

    def get_new(self) -> Score:
        return self.data(0,
                         MatchService().get_new(),
                         PlayerService().get_new(),
                         datetime.now().replace(microsecond=0),
                         None)

    def get_multiple_by_match(self, match: Match) -> [Score]:
        rows: [sqlite3.Row] = self.repository().get_multiple_by_match(match.uid)
        return self.converter().get_data_from_dictionaries(rows)

    def get_multiple_by_player(self, player: Player):
        rows: [sqlite3.Row] = self.repository().get_multiple_by_player(player.uid)
        return self.converter().get_data_from_dictionaries(rows)
