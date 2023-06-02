import pygame
import os
import random

from components.ship import create_enemy_ship,create_asteroid


def spawn_enemy_ships(enemy_ships, spawn_rate, last_spawn_time, stage, pause_duration): #move to ship system file
    current_time = pygame.time.get_ticks() - pause_duration

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



def spawn_asteroids(asteroids, spawn_rate, last_spawn_time, stage, pause_duration): #move to ship system file
    current_time = pygame.time.get_ticks() - pause_duration

    if stage == 1 and current_time - last_spawn_time > spawn_rate:
        # Randomly determine the number of enemy ships to spawns
        num_asteroids = random.randint(0, 2)

        for _ in range(num_asteroids):
            # Create a new enemy ship and append it to the list
            asteroid = create_asteroid()
            asteroids.append(asteroid)

        # Update the last spawn time
        last_spawn_time = current_time

    elif stage == 2 and current_time - last_spawn_time > spawn_rate:
        # Randomly determine the number of enemy ships to spawns
        num_asteroids = random.randint(1, 2)

        for _ in range(num_asteroids):
            # Create a new enemy ship and append it to the list
            asteroid = create_asteroid()
            asteroids.append(asteroid)

        # Update the last spawn time
        last_spawn_time = current_time

    return last_spawn_time