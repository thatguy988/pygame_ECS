import pygame
from components.position import PositionComponent
'''
class MovementSystem:
    @staticmethod
    def move(entity, keys_pressed, width, height, vel, spaceship_width, spaceship_height):
        position_component = entity.get_component(PositionComponent)
        if position_component:
            if keys_pressed[pygame.K_w] and position_component.y > 0: #UP
                position_component.y -= vel
            if keys_pressed[pygame.K_s] and position_component.y < height - spaceship_height:#DOWN
                position_component.y += vel
            if keys_pressed[pygame.K_a] and position_component.x > 0:#LEFT
                position_component.x -= vel
            if keys_pressed[pygame.K_d] and position_component.x < width - spaceship_width:#RIGHT
                position_component.x += vel
'''


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
            if keys_pressed[pygame.K_UP] and position_component.y > 0:  # UP arrow key
                position_component.y -= vel
            if keys_pressed[pygame.K_DOWN] and position_component.y < height - spaceship_height:  # DOWN arrow key
                position_component.y += vel
            if keys_pressed[pygame.K_LEFT] and position_component.x > 0:  # LEFT arrow key
                position_component.x -= vel
            if keys_pressed[pygame.K_RIGHT] and position_component.x < width - spaceship_width:  # RIGHT arrow key
                position_component.x += vel
