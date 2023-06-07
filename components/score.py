
max_points_stage_1 = 100
max_points_stage_2 = 200
max_points_stage_3 = 300 
max_points_stage_4 = 400
max_points_stage_5 = 500
max_points_stage_6 = 600
max_points_stage_7 = 1
max_points_stage_tutorial = 99999


asteroid_points = 10
green_ship_points = 20
orange_ship_points = 5
purple_ship_points = 5
blue_ship_points = 5
brown_ship_points = 5
white_ship_points = 1



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
    

    def reward_points(self, ship_color):
        if ship_color == "grey":
            self.increase_score(asteroid_points)
        elif ship_color == "green":
            self.increase_score(green_ship_points)
        elif ship_color == "orange":
            self.increase_score(orange_ship_points)
        elif ship_color == "purple":
            self.increase_score(purple_ship_points)
        elif ship_color == "blue":
            self.increase_score(blue_ship_points)
        elif ship_color == "brown":
            self.increase_score(brown_ship_points)
        elif ship_color == "white":
            self.increase_score(white_ship_points)
        
    
    @staticmethod
    def set_score_limit(stage):
        if stage == 1:
            return max_points_stage_1
        elif stage == 2:
            return max_points_stage_2
        elif stage == 3:
            return max_points_stage_3
        elif stage == 4:
            return max_points_stage_4
        elif stage == 5:
            return max_points_stage_5
        elif stage == 6:
            return max_points_stage_6
        elif stage == 7:
            return max_points_stage_7
        elif stage == 0:
            return max_points_stage_tutorial
