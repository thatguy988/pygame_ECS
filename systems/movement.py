import pygame
import random
from components.position import PositionComponent



class MovementSystem:
    @staticmethod
    def move_player1(entity, keys_pressed, width, height, vel, spaceship_width, spaceship_height):
        position_component = entity.get_component(PositionComponent)
        if position_component:
            if keys_pressed[pygame.K_w] and position_component.y > 0:  # UP
                position_component.y -= vel
            if keys_pressed[pygame.K_s] and position_component.y < height - spaceship_height:  # DOWN
                position_component.y += vel
            if keys_pressed[pygame.K_a] and position_component.x > 0:  # LEFT
                position_component.x -= vel
            if keys_pressed[pygame.K_d] and position_component.x < width - spaceship_width:  # RIGHT
                position_component.x += vel

    @staticmethod
    def move_player2(entity, keys_pressed, width, height, vel, spaceship_width, spaceship_height):
        position_component = entity.get_component(PositionComponent)
        if position_component:
            if keys_pressed[pygame.K_i] and position_component.y > 0:  # UP arrow key
                position_component.y -= vel
            if keys_pressed[pygame.K_k] and position_component.y < height - spaceship_height:  # DOWN arrow key
                position_component.y += vel
            if keys_pressed[pygame.K_j] and position_component.x > 0:  # LEFT arrow key
                position_component.x -= vel
            if keys_pressed[pygame.K_l] and position_component.x < width - spaceship_width:  # RIGHT arrow key
                position_component.x += vel

    @staticmethod
    def move_enemy_ship(entity, width, vel):
        position_component = entity.get_component(PositionComponent)
        if position_component:
            position_component.x -= vel  # Move the enemy ship to the left

            if position_component.x < -width:
                # Enemy ship reached the left side, generate a new random y-axis position
                position_component.x = width  # Reset x-coordinate to the right side
                position_component.y = random.randint(25, 475)  # Generate a new random y-coordinate