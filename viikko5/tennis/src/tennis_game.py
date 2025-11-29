class TennisGame:
    SCORE = ["Love", "Fifteen", "Thirty", "Forty"]  # points 0,1,2,3
    TIE = ["Love-All", "Fifteen-All", "Thirty-All", "Deuce"]  # tie with points 0,1,2,>3

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.p1_score = 0
        self.p2_score = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.p1_score = self.p1_score + 1
        else:
            self.p2_score = self.p2_score + 1

    def get_score(self):
        if self.p1_score == self.p2_score:
            return self.TIE[self.p1_score] if self.p1_score < 3 else self.TIE[3]

        if self.p1_score >= 4 or self.p2_score >= 4:
            diff = self.p1_score - self.p2_score
            if diff == 1:
                return f"Advantage {self.player1_name}"
            elif diff == -1:
                return f"Advantage {self.player2_name}"
            elif diff >= 2:
                return f"Win for {self.player1_name}"
            else:
                return f"Win for {self.player2_name}"

        return f"{self.SCORE[self.p1_score]}-{self.SCORE[self.p2_score]}"
