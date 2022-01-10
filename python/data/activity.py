from __future__ import annotations

from dataclasses import dataclass

from python.data.generic_data import Data, DataService, _DataConverter, _DataRepository


@dataclass
class Activity(Data):
    uid: int
    name: str

    def get_title(self) -> str:
        return "Aktivität"

    def __str__(self):
        return self.name

    def get_service(self) -> ActivityService:
        return ActivityService()


class _ActivityConverter(_DataConverter):
    def get_data_from_dictionary(self, dictionary: dict) -> Activity:
        return Activity(int(dictionary["uid"]),
                        dictionary["name"])


class _ActivityRepository(_DataRepository):
    table_name = "activity"


class ActivityService(DataService):
    data: Data.__class__ = Activity
    converter: _DataConverter.__class__ = _ActivityConverter
    repository: _DataRepository.__class__ = _ActivityRepository

    def get_new(self) -> Activity:
        return self.data(0,
                         "")
