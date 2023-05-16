import pygame
import os
explosion_images = []

def load_explosion_images():
    for i in range(1, 12):
        image_path = os.path.join('C:/Users/jakob/Desktop/pygame_ECS/Assets/PNG_P/Explosion1', f'Explosion1_{i}.png')
        image = pygame.image.load(image_path).convert_alpha()
        explosion_images.append(image)

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.images = explosion_images
        self.frame_index = 0
        self.frame_count = 0

    def update(self):
        self.frame_count += 1
        if self.frame_count == 11:
            self.frame_index += 1
            self.frame_count = 0

    def draw(self, surface):
        if self.frame_index < len(self.images):
            surface.blit(self.images[self.frame_index], (self.x, self.y))

    def is_finished(self):
        return self.frame_index >= len(self.images)
