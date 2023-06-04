import os
import random
import pygame

from components.position import PositionComponent
GREY = (128,128,128)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
WIDTH, HEIGHT = 1400, 500
GREEN_ENEMY_SHIP_VEL = 3
ASTEROID_VEL = 2
Starting_Position_Width_Player_1, Starting_Position_Height_Player_1 = 100, 150
Starting_Position_Width_Player_2, Starting_Position_Height_Player_2 = 100, 300



class Ship:
    ship_image = pygame.transform.rotate(
        pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'spaceship_grey.png')),
            (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        ),
        90
    )

    def __init__(self, position, image):
        self.position = position
        self.image = image
        self.health = 100
        self.alive = True
        self.visible = True
        self.width = SPACESHIP_WIDTH
        self.height = SPACESHIP_HEIGHT
        self.collision_damage = 0.25

    def stop_moving(self):
        self.velocity = 0
        self.is_moving_up = False
        self.is_moving_down = False
        self.is_moving_left = False
        self.is_moving_right = False

class YellowShip(Ship):
    yellow_ship_image = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))#allow loading og image outside of constructor once then reuse

    def __init__(self, position):
        super().__init__(position, pygame.transform.rotate(pygame.transform.scale(self.yellow_ship_image, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90))

class RedShip(Ship):
    red_ship_image = pygame.image.load(os.path.join('assets', 'spaceship_red.png'))

    def __init__(self, position):
        super().__init__(position, pygame.transform.rotate(pygame.transform.scale(self.red_ship_image, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90))

class EnemyShip(Ship):
    enemy_ship_image = pygame.transform.scale(
        pygame.image.load(os.path.join('assets', 'Ship1.png')),
        (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    )

    def __init__(self, position):
        super().__init__(position, pygame.transform.flip(self.enemy_ship_image, True, False))
        self.health = 10
        self.ship_color = 'green'
        self.velocity = GREEN_ENEMY_SHIP_VEL

class Asteroid(Ship):
    asteroid_image = pygame.image.load(os.path.join('assets', 'asteroid.png'))

    def __init__(self, position):
        super().__init__(position, pygame.transform.rotate(pygame.transform.scale(self.asteroid_image, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 0))
        self.health = random.randint(5, 15)
        self.radius = 30
        self.ship_color = 'grey'
        self.velocity = ASTEROID_VEL

class ShipCreation:
    @staticmethod
    def create_yellow_ship():
        return YellowShip(PositionComponent(Starting_Position_Width_Player_1, Starting_Position_Height_Player_1))

    @staticmethod
    def create_red_ship():
        return RedShip(PositionComponent(Starting_Position_Width_Player_2, Starting_Position_Height_Player_2))

    @staticmethod
    def create_enemy_ship():
        return EnemyShip(PositionComponent(WIDTH, HEIGHT))

    @staticmethod
    def create_asteroid():
        return Asteroid(PositionComponent(WIDTH, HEIGHT))