import pygame
GREY = (128, 128, 128)

class Asteroid:
    def __init__(self, x, y, x_velocity, y_velocity, radius):
        self.x = x
        self.y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.radius = radius
        self.color = GREY  

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)