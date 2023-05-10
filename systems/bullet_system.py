import pygame
from components.bullet import Bullet

class BulletSystem:
    def __init__(self):
        self.bullets = []

    def create_bullet(self, x, y, velocity):
        bullet = Bullet(x, y, velocity)
        self.bullets.append(bullet)

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.x += bullet.velocity

    def remove_offscreen_bullets(self, width):
        self.bullets = [bullet for bullet in self.bullets if bullet.x < width]

    def render_bullets(self, surface, color):
        for bullet in self.bullets:
            pygame.draw.rect(surface, color, (bullet.x, bullet.y, 5, 5))

    def update(self, width, color, surface):
        self.move_bullets()
        self.remove_offscreen_bullets(width)
        self.render_bullets(surface, color)
