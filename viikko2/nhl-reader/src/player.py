class Player:
    def __init__(self, player_dict):
        self.name = player_dict.get("name")
        self.nationality = player_dict.get("nationality")
        self.team = player_dict.get("team")
        self.goals = player_dict.get("goals")
        self.assists = player_dict.get("assists")

    @property
    def points(self):
        return self.goals + self.assists

    def __str__(self):
        return f"{self.name}, ({self.team}), {self.goals}, {self.assists}, {self.points}"
