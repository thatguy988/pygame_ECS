class Score:
    def __init__(self):
        self.score = 0

    def increase_score(self, amount):
        self.score += amount

    def reset_score(self):
        self.score = 0
