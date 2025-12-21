# Kivi-Paperi-Sakset - Testit

## Testien kuvaus

Projekti sisältää kattavat testit kaikille pelin komponenteille:

### 1. Tuomari-testit (`test_tuomari.py`)
- 11 testiä
- Testaa pelilaskurin toimintaa
- Kattaa kaikki voittotilanteet ja tasapelit
- Testaa pisteiden laskentaa

### 2. Tekoäly-testit (`test_tekoaly.py`)
- 15 testiä
- Testaa yksinkertaisen tekoälyn (Tekoaly) siirtojen kierrätystä
- Testaa parannetun tekoälyn (TekoalyParannettu) muistin ja oppimisen
- Varmistaa että tekoälyt toimivat oikein eri tilanteissa

### 3. Peli-testit (`test_kps.py`)
- 16 testiä
- Testaa siirtojen validointia
- Testaa kaikkia pelityyppejä (PvP, AI, Better AI)
- Mockaa käyttäjäsyötteitä

### 4. Web-sovellustestit (`test_web.py`)
- 19 testiä
- Testaa Flask-sovelluksen reitit
- Testaa pelilogiikan web-toteutusta
- Testaa session hallintaa ja käyttöliittymää

## Testien ajaminen

### Kaikki testit
```bash
poetry run pytest src/tests/ -v
```

### Nopea ajo
```bash
poetry run pytest src/tests/ -q
```

### Yksittäinen testitiedosto
```bash
poetry run pytest src/tests/test_tuomari.py -v
```

## Testikattavuus

Yhteensä **61 testiä** kattavat:
- ✅ Tuomari-luokka (100%)
- ✅ Tekoäly-luokat (100%)
- ✅ KPS-peli luokat (100%)
- ✅ Web-sovellus (kaikki reitit ja toiminnallisuudet)

Kaikki testit menevät läpi! 🎉
