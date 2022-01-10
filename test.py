import unittest
from datetime import datetime

from services.database_connection_service import Connection
from data.event import Event, EventService
from data.location import Location, LocationService
from data.match import MatchService
from data.player import PlayerService
from data.score import Score, ScoreService


class TestDb(unittest.TestCase):
    def test_reset_test_data(self):
        con = Connection()
        con.reset_database()
        con.load_test_data()

    def test_get_one_location(self):
        expected: Location = Location(1, "Würfel-Verein Lübeck")
        location: Location = LocationService().get_by_uid(1)
        self.assertEqual(str(location), str(expected))

    def test_get_all_locations(self):
        expected: Location = Location("Club Hamburg")
        locations: [Location] = LocationService().get_all()
        self.assertEqual(str(locations[1]), str(expected))

    def test_get_one_event(self):
        expected: Event = Event(1,
                                "Das Große Turnier",
                                Location(2, 'Club Hamburg'),
                                datetime(2021, 10, 23, 13, 0, 0))
        event: Event = EventService().get_by_uid(1)
        self.assertEqual(str(event), str(expected))

    def test_get_all_events(self):
        expected: Event = Event(2,
                                "Halloween-Würfeln",
                                Location(1, 'Würfel-Verein Lübeck'),
                                datetime(2021, 10, 31, 18, 0, 0))
        events: [Event] = EventService().get_all()
        self.assertEqual(str(events[1]), str(expected))

    def test_get_scores_by_match(self):
        scores: [Score] = ScoreService().get_multiple_by_match(MatchService().get_by_uid(2))
        self.assertEqual(len(scores), 3)
        self.assertEqual(scores[0].score, 48)
        self.assertEqual(scores[1].score, 17)
        self.assertEqual(scores[2].score, 19)

    def test_get_scores_by_player(self):
        scores: [Score] = ScoreService().get_multiple_by_player(PlayerService().get_by_uid(4))
        self.assertEqual(len(scores), 6)
        self.assertEqual(scores[0].score, -8)
        self.assertEqual(scores[0].player.name, "Christa Christensen")
        self.assertEqual(scores[0].match.activity.name, "Kniffel")


if __name__ == '__main__':
    unittest.main()
