import pygame
import random
WIDTH = 10
HEIGHT = 10
class Bullet:
    
    def __init__(self, x, y, x_velocity, y_velocity, radius, owner):
        self.x = x
        self.y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.radius = radius
        self.rect = pygame.Rect(self.x, self.y, WIDTH, HEIGHT) 
        self.active=True
        self.owner = owner


    def update(self, WIDTH):
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.rect.x = self.x

    def get_bullet_damage(self):
        if self.owner == "yellow":
            return 5  # Set the damage value for yellow bullets
        elif self.owner == "red":
            return 5  # Set the damage value for red bullets
        elif self.owner == "green":
            return 8  # Set the damage value for green bullets
        elif self.owner == "orange":
            return 7  # Set the damage value for orange bullets
        elif self.owner == "purple":
            return 6  # Set the damage value for purple bullets
        elif self.owner == "blue":
            return 9  # Set the damage value for blue bullets
        elif self.owner == "brown":
            return 7  # Set the damage value for brown bullets
        elif self.owner == "white":
            return 10  # Set the damage value for white bullets
        else:
            return 0  # Default damage value if owner is not recognized




    
