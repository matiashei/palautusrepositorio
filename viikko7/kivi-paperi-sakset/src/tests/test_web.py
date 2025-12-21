import pytest
from flask import session
from web import app, WebKPS, GAME_TYPES
from kps_tekoaly import KPSTekoaly


@pytest.fixture
def client():
    """Flask test client"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client


@pytest.fixture
def client_with_session(client):
    """Flask test client with session context"""
    with client.session_transaction() as sess:
        sess['game_type'] = 'ai'
        sess['game_name'] = 'Pelaaja vs Tekoäly'
    return client


class TestWebKPS:
    def test_alustus(self):
        """Testaa WebKPS-luokan alustus"""
        game = KPSTekoaly()
        web_kps = WebKPS(game)

        assert web_kps.game is not None
        assert web_kps.tuomari is not None
        assert web_kps.game_over is False

    def test_play_round_ai(self):
        """Testaa yhden kierroksen pelaaminen AI:ta vastaan"""
        game = KPSTekoaly()
        web_kps = WebKPS(game)

        ai_move, error = web_kps.play_round("k")

        assert error is None
        assert ai_move in ["k", "p", "s"]

    def test_play_round_virheellinen_siirto(self):
        """Testaa virheellisen siirron käsittely"""
        game = KPSTekoaly()
        web_kps = WebKPS(game)

        ai_move, error = web_kps.play_round("x")

        assert error is not None
        assert web_kps.game_over is True

    def test_get_score(self):
        """Testaa pisteiden hakeminen"""
        game = KPSTekoaly()
        web_kps = WebKPS(game)

        score = web_kps.get_score()

        assert score['pelaaja1'] == 0
        assert score['pelaaja2'] == 0
        assert score['tasapelit'] == 0

    def test_play_round_paivittaa_pisteet(self):
        """Testaa että kierroksen pelaaminen päivittää pisteet"""
        game = KPSTekoaly()
        web_kps = WebKPS(game)

        # Pelataan kierros
        web_kps.play_round("k")

        score = web_kps.get_score()

        # Pisteet pitäisi olla muuttuneet
        assert (score['pelaaja1'] + score['pelaaja2'] + score['tasapelit']) == 1

    def test_game_paattyy_viiden_voiton_jalkeen(self):
        """Testaa että peli päättyy kun jompikumpi voittaa 5 kierrosta"""
        game = KPSTekoaly()
        web_kps = WebKPS(game)

        # Simuloidaan että pelaaja 1 voittaa 5 kertaa
        # Tekoäly palauttaa: p, s, k, p, s, k...
        # Pelaaja pelaa: k voittaa s (kierros 2, 5, 8, 11, 14)
        for i in range(15):
            if not web_kps.game_over:
                web_kps.play_round("k")

        assert web_kps.game_over is True

    def test_get_winner(self):
        """Testaa get_winner metodin toiminnan"""
        game = KPSTekoaly()
        web_kps = WebKPS(game)

        # Alussa ei voittajaa
        assert web_kps.get_winner() is None

        # Pelataan kunnes pelaaja 1 voittaa
        web_kps.tuomari.ekan_pisteet = 5
        assert web_kps.get_winner() == "Pelaaja 1"

        # Testataan pelaaja 2 voitto
        web_kps.tuomari.ekan_pisteet = 0
        web_kps.tuomari.tokan_pisteet = 5
        assert web_kps.get_winner() == "Pelaaja 2"


class TestIndexRoute:
    def test_index_page(self, client):
        """Testaa etusivu"""
        response = client.get('/')

        assert response.status_code == 200
        assert 'Valitse pelityyppi' in response.data.decode('utf-8')

    def test_index_page_contains_game_types(self, client):
        """Testaa että etusivulla on kaikki pelityypit"""
        response = client.get('/')
        data = response.data.decode('utf-8')

        assert 'Pelaaja vs Pelaaja' in data
        assert 'Tekoäly' in data or 'Tekoaly' in data
        assert 'Parannettu' in data


class TestStartGameRoute:
    def test_start_game_pvp(self, client):
        """Testaa pelin aloitus PvP-tilassa"""
        response = client.get('/start_game/pvp', follow_redirects=True)

        assert response.status_code == 200
        assert 'Pelaaja vs Pelaaja' in response.data.decode('utf-8')

    def test_start_game_ai(self, client):
        """Testaa pelin aloitus AI-tilassa"""
        response = client.get('/start_game/ai', follow_redirects=True)

        assert response.status_code == 200

    def test_start_game_better_ai(self, client):
        """Testaa pelin aloitus parannetun AI:n kanssa"""
        response = client.get('/start_game/better_ai', follow_redirects=True)

        assert response.status_code == 200

    def test_start_game_invalid_type(self, client):
        """Testaa virheellinen pelityyppi"""
        response = client.get('/start_game/invalid', follow_redirects=True)

        # Pitäisi ohjata takaisin etusivulle
        assert response.status_code == 200
        assert 'Valitse pelityyppi' in response.data.decode('utf-8')


class TestGameRoute:
    def test_game_without_session(self, client):
        """Testaa että peli ohjaa etusivulle ilman sessiota"""
        response = client.get('/game', follow_redirects=True)

        assert response.status_code == 200
        assert 'Valitse pelityyppi' in response.data.decode('utf-8')

    def test_game_get_request(self, client):
        """Testaa pelinäkymän GET-pyyntö"""
        # Aloita peli ensin
        client.get('/start_game/ai')

        response = client.get('/game')

        assert response.status_code == 200
        assert 'Pisteet' in response.data.decode('utf-8')

    def test_game_post_request_ai(self, client):
        """Testaa pelikierroksen pelaaminen AI:ta vastaan"""
        # Aloita peli
        client.get('/start_game/ai')

        # Pelaa kierros
        response = client.post('/game', data={'ekan_siirto': 'k'})
        data = response.data.decode('utf-8')

        assert response.status_code == 200
        assert 'Tietokone valitsi' in data or 'Viimeisin kierros' in data

    def test_game_post_request_pvp(self, client):
        """Testaa pelikierroksen pelaaminen PvP-tilassa"""
        # Aloita peli
        client.get('/start_game/pvp')

        # Pelaa kierros
        response = client.post('/game', data={
            'ekan_siirto': 'k',
            'tokan_siirto': 'p'
        })

        assert response.status_code == 200

    def test_game_post_virheellinen_siirto(self, client):
        """Testaa virheellisen siirron käsittely"""
        # Aloita peli
        client.get('/start_game/ai')

        # Yritä pelata virheellinen siirto
        response = client.post('/game', data={'ekan_siirto': 'x'})
        data = response.data.decode('utf-8').lower()

        assert response.status_code == 200
        assert 'virheellinen siirto' in data or 'peli' in data


class TestResetRoute:
    def test_reset(self, client):
        """Testaa pelin nollaus"""
        # Aloita peli
        client.get('/start_game/ai')

        # Nollaa peli
        response = client.get('/reset', follow_redirects=True)

        assert response.status_code == 200
        assert 'Valitse pelityyppi' in response.data.decode('utf-8')


class TestSiirtoNimiFilter:
    def test_siirto_nimi_filter(self):
        """Testaa siirto_nimi Jinja-filtterin"""
        with app.app_context():
            filter_func = app.jinja_env.filters['siirto_nimi']

            assert filter_func('k') == 'Kivi'
            assert filter_func('p') == 'Paperi'
            assert filter_func('s') == 'Sakset'
            assert filter_func('x') == 'x'  # Tuntematon siirto


class TestGameTypes:
    def test_game_types_constant(self):
        """Testaa GAME_TYPES-vakio"""
        assert 'pvp' in GAME_TYPES
        assert 'ai' in GAME_TYPES
        assert 'better_ai' in GAME_TYPES

        assert len(GAME_TYPES['pvp']) == 2
        assert len(GAME_TYPES['ai']) == 2
        assert len(GAME_TYPES['better_ai']) == 2
