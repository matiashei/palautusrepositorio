import pytest
from unittest.mock import patch, MagicMock
from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly
from kps import KiviPaperiSakset


class TestKiviPaperiSakset:
    def test_onko_ok_siirto_kivi(self):
        """Testaa että 'k' on oikea siirto"""
        kps = KPSPelaajaVsPelaaja()
        assert kps._onko_ok_siirto("k") is True

    def test_onko_ok_siirto_paperi(self):
        """Testaa että 'p' on oikea siirto"""
        kps = KPSPelaajaVsPelaaja()
        assert kps._onko_ok_siirto("p") is True

    def test_onko_ok_siirto_sakset(self):
        """Testaa että 's' on oikea siirto"""
        kps = KPSPelaajaVsPelaaja()
        assert kps._onko_ok_siirto("s") is True

    def test_onko_ok_siirto_virheellinen(self):
        """Testaa että virheelliset siirrot eivät ole ok"""
        kps = KPSPelaajaVsPelaaja()
        assert kps._onko_ok_siirto("x") is False
        assert kps._onko_ok_siirto("kivi") is False
        assert kps._onko_ok_siirto("") is False
        assert kps._onko_ok_siirto("K") is False

    def test_tallenna_siirto_perusluokassa(self):
        """Testaa että tallenna_siirto ei tee mitään perusluokassa"""
        kps = KPSPelaajaVsPelaaja()
        # Ei pitäisi nostaa virhettä
        kps._tallenna_siirto("k")


class TestKPSPelaajaVsPelaaja:
    @patch('builtins.input')
    def test_toisen_siirto(self, mock_input):
        """Testaa että toisen pelaajan siirto kysytään"""
        mock_input.return_value = "p"
        kps = KPSPelaajaVsPelaaja()

        siirto = kps._toisen_siirto("k")
        assert siirto == "p"
        mock_input.assert_called_once()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_pelaa_yksi_kierros(self, mock_print, mock_input):
        """Testaa pelikierrosten pelaaminen kunnes jompikumpi voittaa 5 kierrosta"""
        # Simuloidaan että pelaaja 1 voittaa 5 kertaa
        # P1 voittaa: k vs s (5 kertaa)
        mock_input.side_effect = ["k", "s"] * 5

        kps = KPSPelaajaVsPelaaja()
        kps.pelaa()

        # Tarkistetaan että peli päättyi
        assert mock_input.call_count == 10  # 5 kierrosta, 2 syötettä per kierros
    def test_alustus(self):
        """Testaa että tekoäly alustetaan oikein"""
        kps = KPSTekoaly()
        assert kps.tekoaly is not None

    @patch('builtins.print')
    def test_toisen_siirto(self, mock_print):
        """Testaa että tekoälyn siirto palautetaan"""
        kps = KPSTekoaly()

        siirto = kps._toisen_siirto("k")
        assert siirto in ["k", "p", "s"]

        # Tarkistetaan että tekoälyn siirto tulostetaan
        mock_print.assert_called_once()
        assert "Tietokone valitsi:" in str(mock_print.call_args)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_pelaa_yksi_kierros(self, mock_print, mock_input):
        """Testaa pelikierrosten pelaaminen tekoälyä vastaan kunnes 5 voittoa"""
        # Tekoäly palauttaa: p, s, k, p, s, k...
        # P1 pelaa: k voittaa s (kierros 2), s voittaa p (kierros 4)
        # Pelataan kunnes P1 voittaa 5 kertaa
        mock_input.side_effect = ["k"] * 15  # Riittävästi syötteitä

        kps = KPSTekoaly()
        kps.pelaa()

        # Varmistetaan että peliä pelattiin
        assert mock_input.call_count >= 5

    def test_tekoaly_siirrot_kiertavat(self):
        """Testaa että tekoälyn siirrot kiertävät"""
        kps = KPSTekoaly()

        siirrot = []
        for _ in range(3):
            siirrot.append(kps.tekoaly.anna_siirto())

        # Perus tekoäly palauttaa: p, s, k (aloittaa 0:sta, inkrementoi ensin)
        assert siirrot == ["p", "s", "k"]


class TestKPSParempiTekoaly:
    def test_alustus(self):
        """Testaa että parannettu tekoäly alustetaan oikein"""
        kps = KPSParempiTekoaly()
        assert kps.tekoaly is not None

    @patch('builtins.print')
    def test_toisen_siirto(self, mock_print):
        """Testaa että parannetun tekoälyn siirto palautetaan"""
        kps = KPSParempiTekoaly()

        siirto = kps._toisen_siirto("k")
        assert siirto in ["k", "p", "s"]

        # Tarkistetaan että tekoälyn siirto tulostetaan
        mock_print.assert_called_once()
        assert "Tietokone valitsi:" in str(mock_print.call_args)

    def test_tallenna_siirto(self):
        """Testaa että pelaajan siirto tallennetaan tekoälyn muistiin"""
        kps = KPSParempiTekoaly()

        kps._tallenna_siirto("k")
        assert kps.tekoaly._vapaa_muisti_indeksi == 1
        assert kps.tekoaly._muisti[0] == "k"

    @patch('builtins.input')
    @patch('builtins.print')
    def test_pelaa_yksi_kierros(self, mock_print, mock_input):
        """Testaa pelikierrosten pelaaminen parannettua tekoälyä vastaan kunnes 5 voittoa"""
        # Parannettu tekoäly oppii, joten tarvitaan enemmän kierroksia
        mock_input.side_effect = ["k"] * 20  # Riittävästi syötteitä

        kps = KPSParempiTekoaly()
        kps.pelaa()

        # Varmistetaan että peliä pelattiin
        assert mock_input.call_count >= 5

    def test_tekoaly_oppii(self):
        """Testaa että parannettu tekoäly käyttää historiaa"""
        kps = KPSParempiTekoaly()

        # Pelataan useita kierroksia samalla siirtomallilla
        for _ in range(3):
            kps._tallenna_siirto("k")

        # Tekoälyn pitäisi nyt käyttää historiaa
        siirto = kps._toisen_siirto("k")
        assert siirto in ["k", "p", "s"]
