Copilot luetteli muutokset, jotka ohjelmassa oli toteutettu verrattuna main-haarassa olleeseen tehtäväpohjaan. Se huomioi, että:
* luokassa oli otettu käyttöön kaksi listaa pisteille ja pisteille tasatilanteessa toistuvan logiikan korvaamiseksi.
* muuttujat m_score1 ja m_score2 oli vaihdettu helpommin ymmärrettävään muotoon.
* get_score()-metodi oli refaktoroitu lyhyemmäksi ja käyttämään varhaista palautusta.
* voitto- ja etulyöntiasemaviestit oli muokattu vastaamaan pelaajien todellisia nimiä kovakoodattujen nimien sijaan.

Copilot huomautti, että luokkatason muuttumattomien atribuuttien nimet tulisi kirjoittaa isoilla kirjaimilla, eli SCORE ja TIE. Mielestäni huomautus vaikutti aiheelliselta ja Copilotin antama arvio yleensäkin hyödylliseltä, joskin sitä voisi ehkä arvioida paremmin jos koodissa olisi ollut suurempia ongelmia.
