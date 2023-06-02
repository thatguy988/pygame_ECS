class Score:
    def __init__(self, limit):
        self.score = 0
        self.limit = limit
    
    def increase_score(self, amount):
        self.score += amount
    
    def reset_score(self):
        self.score = 0
    
    def has_score_limit_reached(self):
        return self.score >= self.limit
    
    @staticmethod
    def set_score_limit(stage):
        if stage == 1:
            return 100
        elif stage == 2:
            return 200
        elif stage == 3:
            return 300
        elif stage == 4:
            return 400
        elif stage == 5:
            return 500
        elif stage == 6:
            return 600
