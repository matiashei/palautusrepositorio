import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Aapeli", "EDM", 4, 12),
            Player("Eemeli", "PIT", 45, 54),
            Player("Kuukkeli", "EDM", 37, 53),
            Player("Peluri", "DET", 42, 56),
            Player("Huijari", "EDM", 35, 89)
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsService(PlayerReaderStub())

    def test_konstruktori_asettaa_pelaajat_oikein(self):
        self.assertEqual(len(self.stats._players), 5)

    def test_search_palauttaa_oikean_pelaajan(self):
        player = self.stats.search("Huijari")
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Huijari")

    def test_search_palauttaa_none_jos_pelaajaa_ei_loydy(self):
        self.assertIsNone(self.stats.search("Selanne"))

    def test_team_palauttaa_oikean_joukkueen_pelaajat(self):
        names = [p.name for p in self.stats.team("EDM")]
        self.assertEqual(names, ["Aapeli", "Kuukkeli", "Huijari"])

    def test_team_palauttaa_tyhjan_listan_jos_joukkuetta_ei_loydy(self):
        self.assertEqual(self.stats.team("MTL"), [])

    def test_top_palauttaa_oikean_maaran_pelaajia(self):
        top_players = self.stats.top(2)
        self.assertEqual(len(top_players), 3)

    def test_top_palauttaa_pelaajat_pisteiden_mukaan(self):
        top_players = self.stats.top(2)
        self.assertEqual(top_players[0].name, "Huijari")

    def test_top_palauttaa_vain_yhden_jos_how_many_on_nolla(self):
        top_players = self.stats.top(0)
        self.assertEqual(len(top_players), 1)
        self.assertEqual(top_players[0].name, "Huijari")

    def test_top_sort_by_goals(self):
        top_players = self.stats.top(1, sort_by=SortBy.GOALS)
        self.assertEqual(top_players[0].name, "Eemeli")

    def test_top_sort_by_assists(self):
        top_players = self.stats.top(1, sort_by=SortBy.ASSISTS)
        self.assertEqual(top_players[0].name, "Huijari")
