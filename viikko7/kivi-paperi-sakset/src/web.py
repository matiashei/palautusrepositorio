from flask import Flask, render_template, request, session, redirect, url_for
import secrets
from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly
from tuomari import Tuomari

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Pelityypit
GAME_TYPES = {
    'pvp': ('Pelaaja vs Pelaaja', KPSPelaajaVsPelaaja),
    'ai': ('Pelaaja vs Tekoäly', KPSTekoaly),
    'better_ai': ('Pelaaja vs Parannettu Tekoäly', KPSParempiTekoaly)
}

class WebKPS:
    """Luokka, joka käsittelee web-version pelilogiikasta"""
    def __init__(self, game_instance):
        self.game = game_instance
        self.tuomari = Tuomari()
        self.game_over = False
        self.voittoraja = 3

    def play_round(self, ekan_siirto, tokan_siirto=None):
        """Pelaa yhden kierroksen"""
        if not self.game._onko_ok_siirto(ekan_siirto):
            self.game_over = True
            return None, "Virheellinen siirto!"

        # Jos toka siirto ei ole annettu (AI-peli), pyydä se
        if tokan_siirto is None:
            self.game._tallenna_siirto(ekan_siirto)
            tokan_siirto = self.game._toisen_siirto(ekan_siirto)
        elif not self.game._onko_ok_siirto(tokan_siirto):
            self.game_over = True
            return None, "Virheellinen siirto!"

        self.tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)

        # Tarkistetaan onko jompikumpi voittanut 5 kierrosta
        if self.tuomari.ekan_pisteet >= self.voittoraja or self.tuomari.tokan_pisteet >= self.voittoraja:
            self.game_over = True

        return tokan_siirto, None

    def get_winner(self):
        """Palauttaa voittajan nimen tai None jos peli ei ole ohi"""
        if self.tuomari.ekan_pisteet >= self.voittoraja:
            return "Pelaaja 1"
        elif self.tuomari.tokan_pisteet >= self.voittoraja:
            return "Pelaaja 2"
        return None

    def get_score(self):
        return {
            'pelaaja1': self.tuomari.ekan_pisteet,
            'pelaaja2': self.tuomari.tokan_pisteet,
            'tasapelit': self.tuomari.tasapelit
        }

@app.route('/')
def index():
    """Aloitussivu, jossa valitaan pelityyppi"""
    return render_template('index.html', game_types=GAME_TYPES)

@app.route('/start_game/<game_type>')
def start_game(game_type):
    """Aloittaa uuden pelin valitulla pelityypillä"""
    if game_type not in GAME_TYPES:
        return redirect(url_for('index'))

    # Luo uusi peli-instanssi ja tallenna sessioon
    game_class = GAME_TYPES[game_type][1]
    game_instance = game_class()

    # Tallennetaan pelityyppitiedot sessioon
    session['game_type'] = game_type
    session['game_name'] = GAME_TYPES[game_type][0]
    session.modified = True

    # Luodaan WebKPS-instanssi ja tallennetaan app.config:iin
    # (session ei tue monimutkaisempia objekteja suoraan)
    if 'games' not in app.config:
        app.config['games'] = {}

    session_id = session.sid if hasattr(session, 'sid') else id(session)
    app.config['games'][str(session_id)] = WebKPS(game_instance)

    return redirect(url_for('game'))

@app.route('/game', methods=['GET', 'POST'])
def game():
    """Pelinäkymä"""
    if 'game_type' not in session:
        return redirect(url_for('index'))

    session_id = session.sid if hasattr(session, 'sid') else id(session)
    web_kps = app.config.get('games', {}).get(str(session_id))

    if not web_kps:
        return redirect(url_for('index'))

    game_type = session['game_type']
    game_name = session['game_name']
    is_pvp = (game_type == 'pvp')

    message = None
    last_round = None

    if request.method == 'POST':
        ekan_siirto = request.form.get('ekan_siirto', '').lower()

        if is_pvp:
            tokan_siirto = request.form.get('tokan_siirto', '').lower()
            ai_move, error = web_kps.play_round(ekan_siirto, tokan_siirto)
            if error:
                message = error
            else:
                last_round = {
                    'pelaaja1': ekan_siirto,
                    'pelaaja2': tokan_siirto
                }
        else:
            ai_move, error = web_kps.play_round(ekan_siirto)
            if error:
                message = error
            else:
                last_round = {
                    'pelaaja1': ekan_siirto,
                    'pelaaja2': ai_move
                }

    score = web_kps.get_score()
    game_over = web_kps.game_over
    winner = web_kps.get_winner()

    return render_template('game.html',
                         game_name=game_name,
                         is_pvp=is_pvp,
                         score=score,
                         message=message,
                         last_round=last_round,
                         game_over=game_over,
                         winner=winner,
                         voittoraja=web_kps.voittoraja)

@app.route('/reset')
def reset():
    """Nollaa pelin"""
    session_id = session.sid if hasattr(session, 'sid') else id(session)
    if str(session_id) in app.config.get('games', {}):
        del app.config['games'][str(session_id)]
    session.clear()
    return redirect(url_for('index'))

def siirto_nimi(siirto):
    """Apufunktio, joka palauttaa siirron nimen"""
    siirrot = {'k': 'Kivi', 'p': 'Paperi', 's': 'Sakset'}
    return siirrot.get(siirto, siirto)

app.jinja_env.filters['siirto_nimi'] = siirto_nimi

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
