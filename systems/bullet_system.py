import pygame
from components.bullet import Bullet
from components.dimension import Dimensions

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

    def remove_offscreen_bullets(self, width):
        self.bullets = [bullet for bullet in self.bullets if bullet.x < width]

    def render_bullets(self, surface, color):
        for bullet in self.bullets:
            pygame.draw.rect(surface, color, (bullet.x, bullet.y, 5, 5))

    def update(self, width, color, surface):
        self.move_bullets()
        self.remove_offscreen_bullets(width)
        self.render_bullets(surface, color)

    def auto_fire(self, ship_entity, velocity, radius):
        x = ship_entity.position.x + ship_entity.width  # Adjust the position as needed
        y = ship_entity.position.y + ship_entity.height // 2  # Adjust the position as needed
        self.create_bullet(x, y, velocity, radius)

        
