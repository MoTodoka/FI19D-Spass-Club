from __future__ import annotations

from dataclasses import dataclass

from python.data.generic_data import Data, DataService, _DataConverter, _DataRepository


@dataclass
class Location(Data):
    uid: int
    name: str

    def get_title(self) -> str:
        return "Ort"

    def __str__(self):
        return self.name

    def get_service(self) -> LocationService:
        return LocationService()


class _LocationConverter(_DataConverter):
    def get_data_from_dictionary(self, dictionary: dict) -> Location:
        return Location(int(dictionary["uid"]),
                        dictionary["name"])


class _LocationRepository(_DataRepository):
    table_name = "location"


class LocationService(DataService):
    data: Data.__class__ = Location
    converter: _DataConverter.__class__ = _LocationConverter
    repository: _DataRepository.__class__ = _LocationRepository

    def get_new(self) -> Location:
        return self.data(0,
                         "")
