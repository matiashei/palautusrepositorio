import pytest
from tuomari import Tuomari


class TestTuomari:
    def setup_method(self):
        """Alustetaan tuomari ennen jokaista testiä"""
        self.tuomari = Tuomari()

    def test_alustus(self):
        """Testaa että tuomari alustetaan oikein"""
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0

    def test_tasapeli(self):
        """Testaa tasapelitilanne"""
        self.tuomari.kirjaa_siirto("k", "k")
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 1

    def test_eka_voittaa_kivi_voittaa_sakset(self):
        """Testaa että kivi voittaa sakset"""
        self.tuomari.kirjaa_siirto("k", "s")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0

    def test_eka_voittaa_paperi_voittaa_kiven(self):
        """Testaa että paperi voittaa kiven"""
        self.tuomari.kirjaa_siirto("p", "k")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0

    def test_eka_voittaa_sakset_voittaa_paperin(self):
        """Testaa että sakset voittaa paperin"""
        self.tuomari.kirjaa_siirto("s", "p")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0

    def test_toka_voittaa_kivi_voittaa_sakset(self):
        """Testaa että toisen pelaajan kivi voittaa sakset"""
        self.tuomari.kirjaa_siirto("s", "k")
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 0

    def test_toka_voittaa_paperi_voittaa_kiven(self):
        """Testaa että toisen pelaajan paperi voittaa kiven"""
        self.tuomari.kirjaa_siirto("k", "p")
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 0

    def test_toka_voittaa_sakset_voittaa_paperin(self):
        """Testaa että toisen pelaajan sakset voittaa paperin"""
        self.tuomari.kirjaa_siirto("p", "s")
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 0

    def test_useita_kierroksia(self):
        """Testaa useita pelikierroksia"""
        self.tuomari.kirjaa_siirto("k", "s")  # Eka voittaa
        self.tuomari.kirjaa_siirto("p", "k")  # Eka voittaa
        self.tuomari.kirjaa_siirto("s", "k")  # Toka voittaa
        self.tuomari.kirjaa_siirto("k", "k")  # Tasapeli

        assert self.tuomari.ekan_pisteet == 2
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 1

    def test_str_metodi(self):
        """Testaa että __str__ palauttaa oikean muotoisen merkkijonon"""
        self.tuomari.kirjaa_siirto("k", "s")
        self.tuomari.kirjaa_siirto("p", "p")

        tulos = str(self.tuomari)
        assert "1 - 0" in tulos
        assert "Tasapelit: 1" in tulos

    def test_kaikki_tasapelit(self):
        """Testaa kaikki tasapeliyhdistelmät"""
        tasapelit = [("k", "k"), ("p", "p"), ("s", "s")]

        for eka, toka in tasapelit:
            tuomari = Tuomari()
            tuomari.kirjaa_siirto(eka, toka)
            assert tuomari.tasapelit == 1
            assert tuomari.ekan_pisteet == 0
            assert tuomari.tokan_pisteet == 0
