import pygame

class MovementSystem:
    @staticmethod
    def move(entity, keys_pressed, WIDTH, HEIGHT, VEL, SPACESHIP_WIDTH, SPACESHIP_HEIGHT):
        if keys_pressed[pygame.K_a] and entity.position.x - VEL > 0:
            entity.position.x -= VEL
        if keys_pressed[pygame.K_d] and entity.position.x + SPACESHIP_WIDTH < WIDTH:
            entity.position.x += VEL
        if keys_pressed[pygame.K_w] and entity.position.y - VEL > 0:
            entity.position.y -= VEL
        if keys_pressed[pygame.K_s] and entity.position.y + SPACESHIP_HEIGHT + VEL < HEIGHT - 15:
            entity.position.y += VEL
