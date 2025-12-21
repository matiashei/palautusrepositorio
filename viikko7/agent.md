Agentin tekemä ratkaisu on vaikuttaa mielestäni toimivalta, pyrin varmistamaan toimivuuden käymällä testit läpi sekä testaamalla käyttöliittymää manuaalisesti. En joutunut pyytämään agenttia korjaamaan sen toteuttamaa ratkaisua kertaakaan, komentoja annoin yhteensä 4. 

Myös agentin kirjoittamat testit vaikuttavat toimivilta, joskin agentti lisäsi hieman hölmösti jokaiselle testille kommenttina selityksen sen tehtävästä, vaikka testien nimet selittävät pääosin melko tyhjentävästi niiden tarkoituksen (niissä kohdissa, joissa eivät selitä, parempi käytäntö olisi muuttaa nimeämiskäytäntöä). Esimerkiksi:
```
    def test_onko_ok_siirto_kivi(self):
        """Testaa että 'k' on oikea siirto"""
        kps = KPSPelaajaVsPelaaja()
        assert kps._onko_ok_siirto("k") is True
  ```

Agentin kirjoittama koodi on pääosin ymmärrettävää, joskin html-tiedostoissa on jonkin verran JavaScriptia, jota tunnen itse toistaiseksi melko heikosti, enkä ymmärtänyt näitä osioita tiedostoista täydellisesti. Agentti piti edellisessä tehtävässä luodun koodin melko samanlaisena: se muokkasi index.py-tiedostoon tulostuksen uudesta pelilogiikasta (5 kierrosvoittoa ja pelaaja voittaa koko pelin) ja lisäsi kps.py-tiedostoon tarkistuksen kierrosvoitoista. Sen lisäksi agentti loi web.py-tiedoston, joka ajaa web-liittymän, joukon html-tiedostoja sekä testit ja niiden dokumentaation erilliseen md-tiedostoon.

Opin, että agentin avulla sovellusta voi laajentaa nopeasti. Itse käyttäisin agentin luomaa laajennusta pohjana, jota lähtisin konfiguroimaan käsin ja agentin avustuksella pidemmälle.
