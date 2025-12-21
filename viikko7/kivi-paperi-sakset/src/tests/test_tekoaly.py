import pytest
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu


class TestTekoaly:
    def setup_method(self):
        """Alustetaan tekoäly ennen jokaista testiä"""
        self.tekoaly = Tekoaly()

    def test_alustus(self):
        """Testaa että tekoäly alustetaan oikein"""
        assert self.tekoaly._siirto == 0

    def test_anna_siirto_palauttaa_oikean_siirron(self):
        """Testaa että tekoäly palauttaa siirtoja kierroksittain"""
        siirrot = []
        for _ in range(6):
            siirrot.append(self.tekoaly.anna_siirto())

        # Tekoälyn pitäisi palauttaa: p, s, k, p, s, k (aloittaa 0:sta, inkrementoi ensin)
        assert siirrot == ["p", "s", "k", "p", "s", "k"]

    def test_anna_siirto_ensimmainen_siirto(self):
        """Testaa ensimmäinen siirto"""
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "p"

    def test_anna_siirto_toinen_siirto(self):
        """Testaa toinen siirto"""
        self.tekoaly.anna_siirto()
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "s"

    def test_anna_siirto_kolmas_siirto(self):
        """Testaa kolmas siirto"""
        self.tekoaly.anna_siirto()
        self.tekoaly.anna_siirto()
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "k"

    def test_aseta_siirto_ei_tee_mitaan(self):
        """Testaa että aseta_siirto ei vaikuta mihinkään"""
        siirto_ennen = self.tekoaly.anna_siirto()
        self.tekoaly.aseta_siirto("p")
        siirto_jalkeen = self.tekoaly.anna_siirto()

        # Siirtojen pitäisi jatkua normaalisti
        assert siirto_ennen == "p"
        assert siirto_jalkeen == "s"


class TestTekoalyParannettu:
    def setup_method(self):
        """Alustetaan parannettu tekoäly ennen jokaista testiä"""
        self.tekoaly = TekoalyParannettu(10)

    def test_alustus(self):
        """Testaa että parannettu tekoäly alustetaan oikein"""
        assert len(self.tekoaly._muisti) == 10
        assert self.tekoaly._vapaa_muisti_indeksi == 0

    def test_anna_siirto_ilman_historiaa(self):
        """Testaa että tekoäly palauttaa 'k' kun ei ole historiaa"""
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "k"

    def test_anna_siirto_yhdella_siirtolla(self):
        """Testaa että tekoäly palauttaa 'k' kun on vain yksi siirto muistissa"""
        self.tekoaly.aseta_siirto("p")
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "k"

    def test_aseta_siirto_tallentaa_muistiin(self):
        """Testaa että siirrot tallentuvat muistiin"""
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.aseta_siirto("p")
        self.tekoaly.aseta_siirto("s")

        assert self.tekoaly._muisti[0] == "k"
        assert self.tekoaly._muisti[1] == "p"
        assert self.tekoaly._muisti[2] == "s"
        assert self.tekoaly._vapaa_muisti_indeksi == 3

    def test_muisti_tayttyy(self):
        """Testaa että vanha siirto unohdetaan kun muisti täyttyy"""
        # Täytetään muisti
        for i in range(11):
            self.tekoaly.aseta_siirto("k")

        # Muistin koko on 10, joten ensimmäinen pitäisi olla unohtunut
        assert self.tekoaly._vapaa_muisti_indeksi == 10
        assert all(siirto == "k" for siirto in self.tekoaly._muisti)

    def test_anna_siirto_perustuu_historiaan(self):
        """Testaa että tekoäly käyttää historiaa päätöksenteossaan"""
        # Simuloidaan tilanne jossa vastustaja pelaa usein kiven paperin jälkeen
        self.tekoaly.aseta_siirto("p")
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.aseta_siirto("p")
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.aseta_siirto("p")

        # Tekoälyn pitäisi nyt olettaa että vastustaja pelaa kiven
        # ja vastata siihen paperilla
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "p"

    def test_anna_siirto_paperi_historia(self):
        """Testaa että tekoäly vastaa saksilla jos papereita eniten"""
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.aseta_siirto("p")
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.aseta_siirto("p")
        self.tekoaly.aseta_siirto("k")

        siirto = self.tekoaly.anna_siirto()
        assert siirto == "s"

    def test_anna_siirto_sakset_historia(self):
        """Testaa että tekoäly vastaa kivellä jos ei kiviä eikä papereita eniten"""
        self.tekoaly.aseta_siirto("p")
        self.tekoaly.aseta_siirto("s")
        self.tekoaly.aseta_siirto("p")
        self.tekoaly.aseta_siirto("s")
        self.tekoaly.aseta_siirto("p")

        siirto = self.tekoaly.anna_siirto()
        assert siirto == "k"

    def test_eri_muistikoot(self):
        """Testaa että tekoäly toimii eri muistikoilla"""
        for koko in [1, 5, 20]:
            tekoaly = TekoalyParannettu(koko)
            assert len(tekoaly._muisti) == koko
            assert tekoaly.anna_siirto() in ["k", "p", "s"]
