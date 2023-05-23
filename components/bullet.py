import pygame
WIDTH = 10
HEIGHT = 10
class Bullet:
    
    def __init__(self, x, y, velocity,radius):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.radius = radius
        self.rect = pygame.Rect(self.x, self.y, WIDTH, HEIGHT) 
        self.active=True


    def update(self, WIDTH):
        self.x += self.velocity
        self.rect.x = self.x
