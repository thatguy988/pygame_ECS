import os
import random
import pygame

from components.position import PositionComponent
GREY = (128,128,128)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
WIDTH, HEIGHT = 1400, 500

DEFAULT_HEALTH = 100
player_bullet_damage = 5

green_enemy_ship_bullet_damage = 5

orange_enemy_ship_bullet_damage = 10



GREEN_ENEMY_SHIP_HEALTH = 10
GREEN_ENEMY_SHIP_VEL = 3

orange_enemy_ship_health = 20
orange_enemy_ship_vel = 2

ASTEROID_VEL = 2
ASTEROID_RADIUS = 30
ASTEROID_HEALTH_MIN = 5
ASTEROID_HEALTH_MAX = 15

COLLISION_DAMAGE = 0.25

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
        self.health = DEFAULT_HEALTH
        self.alive = True
        self.visible = True
        self.width = SPACESHIP_WIDTH
        self.height = SPACESHIP_HEIGHT
        self.collision_damage = COLLISION_DAMAGE
        self.bullet_damage = player_bullet_damage

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
        self.initial_health = GREEN_ENEMY_SHIP_HEALTH
        self.health=self.initial_health
        self.ship_color = 'green'
        self.velocity = GREEN_ENEMY_SHIP_VEL
        self.bullet_damage = green_enemy_ship_bullet_damage 

class OrangeEnemyShip(Ship):
    enemy_ship_image = pygame.transform.scale(
        pygame.image.load(os.path.join('assets', 'Ship4.png')),
        (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    )

    def __init__(self, position):
        super().__init__(position, pygame.transform.flip(self.enemy_ship_image, True, False))
        self.initial_health = orange_enemy_ship_health
        self.health=self.initial_health
        self.ship_color = 'orange'
        self.velocity = orange_enemy_ship_vel
        self.bullet_damage = orange_enemy_ship_bullet_damage


class Asteroid(Ship):
    asteroid_image = pygame.image.load(os.path.join('assets', 'asteroid.png'))

    def __init__(self, position):
        super().__init__(position, pygame.transform.rotate(pygame.transform.scale(self.asteroid_image, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 0))
        self.initial_health = random.randint(ASTEROID_HEALTH_MIN, ASTEROID_HEALTH_MAX)
        self.health = self.initial_health
        self.radius = ASTEROID_RADIUS
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
    def create_orange_enemy_ship():
        return OrangeEnemyShip(PositionComponent(WIDTH, HEIGHT))

    @staticmethod
    def create_asteroid():
        return Asteroid(PositionComponent(WIDTH, HEIGHT))
    