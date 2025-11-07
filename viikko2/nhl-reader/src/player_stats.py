class PlayerStats:
    def __init__(self, reader):
        self.reader = reader

    def top_scorers_by_nationality(self, nationality):
        players = []
        for player in self.reader.get_players():
            if player.nationality == nationality:
                players.append(player)
        players.sort(key=lambda p: p.points, reverse=True)
        return players
