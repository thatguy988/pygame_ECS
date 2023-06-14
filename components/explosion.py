import pygame
import os

class Explosion:
    explosion_images = []

    @classmethod
    def load_explosion_images(cls):
        if not cls.explosion_images:  
            for i in range(1, 12):
                image_path = os.path.join('C:/Users/jakob/Desktop/pygame_ECS/Assets/PNG_Parts&Spriter_Animation/Explosions/Explosion1', f'Explosion1_{i}.png')
                image = pygame.image.load(image_path).convert_alpha()
                cls.explosion_images.append(image)
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.images = Explosion.explosion_images
        self.frame_index = 0
        self.frame_count = 0
        
    def update(self):
        self.frame_count += 1
        if self.frame_count >= 7:
            self.frame_index += 1
            self.frame_count = 0

    def is_finished(self):
        return self.frame_index >= len(self.images)
    
    def remove(self, explosions):
        explosions.remove(self)
