import pygame
import os
import random

from components.position import PositionComponent

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
WIDTH, HEIGHT = 1400, 500
class Ship:
    def __init__(self, position, image_path):
        self.position = position
        self.image = pygame.transform.rotate(
            pygame.transform.scale(
                pygame.image.load(image_path),
                (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
            ),
            90
        )
        self.health = 100
        self.alive = True
        self.visible = True

    def stop_moving(self):#used by enemy ship
        # Stop the movement of the entity
        # Assuming you have a velocity attribute, you can set it to zero
        self.velocity = 0
        # If you have movement flags, you can set them to False
        self.is_moving_up = False
        self.is_moving_down = False
        self.is_moving_left = False
        self.is_moving_right = False
        

class YellowShip(Ship):
    def __init__(self, position):
        super().__init__(position, os.path.join('assets', 'spaceship_yellow.png'))


class RedShip(Ship):
    def __init__(self, position):
        super().__init__(position, os.path.join('assets', 'spaceship_red.png'))


class EnemyShip(Ship):
    def __init__(self, position):
        super().__init__(position, os.path.join('assets', 'Ship1.png'))
        self.health = 10  # override initial health value for the enemy ship

        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'Ship1.png')),
            (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        )# Override the rotation angle for the image
        


        
        self.image = pygame.transform.flip(self.image, True, False)# Flip the image horizontally


def create_yellow_ship():
    yellow = YellowShip(PositionComponent(100, 150))
    return yellow


def create_red_ship():
    red = RedShip(PositionComponent(100, 300))
    return red


def create_enemy_ship():
    enemy_ship = EnemyShip(PositionComponent(WIDTH, HEIGHT))
    return enemy_ship



def spawn_enemy_ships(enemy_ships, spawn_rate, last_spawn_time, stage): #move to ship system file
    current_time = pygame.time.get_ticks()

    if stage == 1 and current_time - last_spawn_time > spawn_rate:
        # Randomly determine the number of enemy ships to spawns
        num_ships = random.randint(0, 2)

        for _ in range(num_ships):
            # Create a new enemy ship and append it to the list
            new_enemy_ship = create_enemy_ship()
            enemy_ships.append(new_enemy_ship)

        # Update the last spawn time
        last_spawn_time = current_time

    elif stage == 2 and current_time - last_spawn_time > spawn_rate:
        # Randomly determine the number of enemy ships to spawn
        num_ships = random.randint(1, 2)

        for _ in range(num_ships):
            # Create a new enemy ship and append it to the list
            new_enemy_ship = create_enemy_ship()
            enemy_ships.append(new_enemy_ship)

        # Update the last spawn time
        last_spawn_time = current_time

    return last_spawn_time