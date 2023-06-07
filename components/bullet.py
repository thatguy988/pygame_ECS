import pygame
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
