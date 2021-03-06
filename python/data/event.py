from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from python.data.generic_data import Data, DataService, _DataConverter, _DataDbConnection
from python.data.location import Location, LocationService


@dataclass
class Event(Data):
    uid: int
    name: str
    location: Location
    timestamp: datetime

    def get_title(self) -> str:
        return "Event"

    def __str__(self):
        return self.name

    def get_service(self) -> EventService:
        return EventService()


class _EventConverter(_DataConverter):
    def get_data_from_dictionary(self, dictionary: dict) -> Event:
        return Event(int(dictionary["uid"]),
                     dictionary["name"],
                     LocationService().get_by_uid(dictionary["location"]),
                     self.get_date_time_from(dictionary["timestamp"]))


class _EventDbConnection(_DataDbConnection):
    table_name = "event"


class EventService(DataService):
    data: Data.__class__ = Event
    converter: _DataConverter.__class__ = _EventConverter
    repository: _DataDbConnection.__class__ = _EventDbConnection

    def get_new(self) -> Event:
        return self.data(0,
                         "",
                         LocationService().get_new(),
                         datetime.now().replace(microsecond=0))
