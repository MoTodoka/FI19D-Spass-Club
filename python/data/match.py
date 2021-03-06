from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from python.services.database_connection_service import *

from python.data.activity import Activity, ActivityService
from python.data.activity import Data, DataService, _DataConverter, _DataDbConnection
from python.data.event import Event, EventService
from python.data.location import Location, LocationService


@dataclass
class Match(Data):
    uid: int
    timestamp: datetime
    activity: Activity
    location: Location
    event: Event

    def get_title(self) -> str:
        return "Runde"

    def __str__(self):
        return f"{self.timestamp} - {self.activity} - {self.location} ({self.event})"

    def get_service(self) -> MatchService:
        return MatchService()


class _MatchConverter(_DataConverter):
    def get_data_from_dictionary(self, dictionary: dict) -> Match:
        return Match(int(dictionary["uid"]),
                     self.get_date_time_from(dictionary["timestamp"]),
                     ActivityService().get_by_uid(dictionary["activity"]),
                     LocationService().get_by_uid(dictionary["location"]),
                     EventService().get_by_uid(dictionary["event"])
                     if dictionary["event"] is not None
                     else EventService().get_new())


class _MatchDbConnection(_DataDbConnection):
    table_name = "match"

    def get_multiple_by_event(self, event_uid: int) -> [sqlite3.Row]:
        cur = self.con.sqlite3_con.cursor()
        cur.execute('''SELECT * FROM match WHERE event = ?;''', (str(event_uid),))
        return cur.fetchall()


class MatchService(DataService):
    data: Data.__class__ = Match
    converter: _DataConverter.__class__ = _MatchConverter
    repository: _DataDbConnection.__class__ = _MatchDbConnection

    def get_new(self) -> Match:
        return self.data(0,
                         datetime.now().replace(microsecond=0),
                         ActivityService().get_new(),
                         LocationService().get_new(),
                         EventService().get_new())

    def get_multiple_by_event(self, event) -> [Match]:
        rows: [sqlite3.Row] = self.repository().get_multiple_by_event(event.uid)
        return self.converter().get_data_from_dictionaries(rows)
