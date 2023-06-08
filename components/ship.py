import os
import random
import pygame

from components.position import PositionComponent
GREY = (128,128,128)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
BOSS_SHIP_WIDTH, BOSS_SHIP_HEIGHT = 200,200
WIDTH, HEIGHT = 1400, 500
maximum_y_value = HEIGHT - 25
minimum_y_value = HEIGHT - maximum_y_value


DEFAULT_HEALTH = 100


purple_enemy_ship_health = 30
purple_enemy_ship_velocity = 4

blue_enemy_ship_health = 20
blue_enemy_ship_velocity = 8


brown_enemy_ship_health = 20
brown_enemy_ship_velocity = 3


boss_enemy_ship_health = 1000
boss_enemy_ship_velocity = 1


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

class GreenEnemyShip(Ship):
    enemy_ship_image = pygame.transform.scale(
        pygame.image.load(os.path.join('assets/PNG_Parts&Spriter_Animation/Ship1', 'Ship1.png')),
        (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    )

    def __init__(self, position):
        super().__init__(position, pygame.transform.flip(self.enemy_ship_image, True, False))
        self.initial_health = GREEN_ENEMY_SHIP_HEALTH
        self.health=self.initial_health
        self.ship_color = 'green'
        self.velocity = GREEN_ENEMY_SHIP_VEL 

class OrangeEnemyShip(Ship):
    enemy_ship_image = pygame.transform.scale(
        pygame.image.load(os.path.join('assets/PNG_Parts&Spriter_Animation/Ship4', 'Ship4.png')),
        (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    )

    def __init__(self, position):
        super().__init__(position, pygame.transform.flip(self.enemy_ship_image, True, False))
        self.initial_health = orange_enemy_ship_health
        self.health=self.initial_health
        self.ship_color = 'orange'
        self.velocity = orange_enemy_ship_vel

class PurpleEnemyShip(Ship):
    enemy_ship_image = pygame.transform.scale(
        pygame.image.load(os.path.join('assets/PNG_Parts&Spriter_Animation/Ship2', 'Ship2.png')),
        (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    )

    def __init__(self, position):
        super().__init__(position, pygame.transform.flip(self.enemy_ship_image, True, False))
        self.initial_health = purple_enemy_ship_health
        self.health=self.initial_health
        self.ship_color = 'purple'
        self.velocity = purple_enemy_ship_velocity
        self.bullet_switch = True

class BlueEnemyShip(Ship):
    enemy_ship_image = pygame.transform.scale(
        pygame.image.load(os.path.join('assets/PNG_Parts&Spriter_Animation/Ship5', 'Ship5.png')),
        (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    )

    def __init__(self, position):
        super().__init__(position, pygame.transform.flip(self.enemy_ship_image, True, False))
        self.initial_health = blue_enemy_ship_health
        self.health=self.initial_health
        self.ship_color = 'blue'
        self.velocity = blue_enemy_ship_velocity
        

class BrownEnemyShip(Ship):
    enemy_ship_image = pygame.transform.scale(
        pygame.image.load(os.path.join('assets/PNG_Parts&Spriter_Animation/Ship6', 'Ship6.png')),
        (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    )

    def __init__(self, position):
        super().__init__(position, pygame.transform.flip(self.enemy_ship_image, True, False))
        self.initial_health = brown_enemy_ship_health
        self.health=self.initial_health
        self.ship_color = 'brown'
        self.velocity = brown_enemy_ship_velocity

class BossEnemyShip(Ship):
    enemy_ship_image = pygame.transform.scale(
        pygame.image.load(os.path.join('assets/PNG_Parts&Spriter_Animation/Ship3', 'Ship3.png')),
        (BOSS_SHIP_WIDTH, BOSS_SHIP_HEIGHT)
    )

    def __init__(self, position):
        super().__init__(position, pygame.transform.flip(self.enemy_ship_image, True, False))
        self.initial_health = boss_enemy_ship_health
        self.health=self.initial_health
        self.ship_color = 'white'
        self.velocity = boss_enemy_ship_velocity
        #attributes for bullet behavior of ship
        self.bullet_change = random.randint(0,2)
        self.bullet_beam = 0
        self.beam_1_y_position=0
        self.beam_2_y_position=0
        self.beam_3_y_position=0
        self.beam_4_y_position=0
        self.beam_5_y_position=0
        self.bullet_count= 0
        self.bullet_count_limit = random.randint(20,35)
        
        

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
    def create_green_enemy_ship():
        return GreenEnemyShip(PositionComponent(WIDTH, random.randint(minimum_y_value, maximum_y_value)))
    
    @staticmethod
    def create_orange_enemy_ship():
        return OrangeEnemyShip(PositionComponent(WIDTH, random.randint(minimum_y_value, maximum_y_value)))
    
    @staticmethod
    def create_purple_enemy_ship():
        return PurpleEnemyShip(PositionComponent(WIDTH, random.randint(minimum_y_value, maximum_y_value)))
    
    @staticmethod
    def create_blue_enemy_ship():
        return BlueEnemyShip(PositionComponent(WIDTH, random.randint(minimum_y_value, maximum_y_value)))
    
    @staticmethod
    def create_brown_enemy_ship():
        return BrownEnemyShip(PositionComponent(WIDTH, random.randint(minimum_y_value, maximum_y_value)))
    
    @staticmethod
    def create_boss_enemy_ship():
        return BossEnemyShip(PositionComponent(WIDTH, HEIGHT / 2))
    
    @staticmethod
    def create_asteroid():
        return Asteroid(PositionComponent(WIDTH, random.randint(minimum_y_value, maximum_y_value)))
    