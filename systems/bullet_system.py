import pygame
from components.bullet import Bullet
from components.dimension import Dimensions
import time
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

class BulletSystem:
    def __init__(self):
        self.bullets = []

    def create_bullet(self, x, y, velocity, radius):
        bullet = Bullet(x, y, velocity, radius)
        self.bullets.append(bullet)

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.x += bullet.velocity

    def remove_bullet(self, bullet):
        self.bullets.remove(bullet)
        #bullet.active=False

    def remove_offscreen_bullets(self, width):
        self.bullets = [bullet for bullet in self.bullets if bullet.x < width]

    def render_bullets(self, surface, color):
        for bullet in self.bullets:
            #if bullet.active:
            pygame.draw.rect(surface, color, (bullet.x, bullet.y, 5, 5))

    def update(self, width, color, surface):
        self.move_bullets()
        self.remove_offscreen_bullets(width)
        self.render_bullets(surface, color)

    

    def auto_fire(self, entities, velocity, radius, delay):
        current_time = time.time()
        last_fire_times = {}  # Dictionary to store the last fire time for each entity

        for entity in entities:
            last_fire_time = last_fire_times.get(entity, 600)
            if current_time - last_fire_time >= delay:
                x = entity.position.x  # Adjust the position as needed
                y = entity.position.y + entity.height // 2  # Adjust the position as needed
                self.create_bullet(x, y, velocity, radius)
                last_fire_times[entity] = current_time

'''
    def auto_fire(self, entities, velocity, radius):
        for entity in entities:
            x = entity.position.x   # Adjust the position as needed
            y = entity.position.y + entity.height // 2  # Adjust the position as needed
            self.create_bullet(x, y, velocity, radius)
'''



        
