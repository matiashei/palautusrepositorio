from kps import KiviPaperiSakset

class KPSPelaajaVsPelaaja(KiviPaperiSakset):
    def _toisen_siirto(self, _ensimmaisen_siirto):
        return input("Toisen pelaajan siirto: ")
