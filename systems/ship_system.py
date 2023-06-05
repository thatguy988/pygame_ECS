import pygame
import random

from components.ship import ShipCreation


asteroid_spawn_rate = 3000 # spawn time interval

green_ship_spawn_rate = 5000  # Time interval (in milliseconds) between enemy ship spawns


orange_ship_spawn_rate = 1000

green_ship_min_stage_1 = 0
green_ship_max_stage_1 = 2

green_ship_min_stage_2 = 1
green_ship_max_stage_2 = 2


orange_min_stage_1 = 0
orange_max_stage_1 = 1
orange_min_stage_2 = 1
orange_max_stage_2 = 2



asteroid_min_stage_1 = 1
asteroid_max_stage_1 = 2
asteroid_min_stage_2 = 0
asteroid_max_stage_2 = 1
asteroid_min_stage_8 = 1
asteroid_max_stage_8 = 2

def create_ships(enemy_ships,last_spawn_time_green_ships,last_spawn_time_orange_ships,last_asteroid_spawn_time,stage,pause_duration):
    if stage == 1:
        last_spawn_time_green_ships = SpawnSystem.spawn_enemy_ships(enemy_ships, green_ship_spawn_rate, last_spawn_time_green_ships,stage, pause_duration)
        last_asteroid_spawn_time = SpawnSystem.spawn_asteroids(enemy_ships, asteroid_spawn_rate, last_asteroid_spawn_time,stage, pause_duration)
        #last_spawn_time_orange_ships = SpawnSystem.spawn_orange_enemy_ships(enemy_ships,orange_ship_spawn_rate,last_spawn_time_orange_ships,stage, pause_duration)



        return last_spawn_time_green_ships, last_spawn_time_orange_ships, last_asteroid_spawn_time
    elif stage == 2:
        last_spawn_time_green_ships = SpawnSystem.spawn_enemy_ships(enemy_ships, green_ship_spawn_rate, last_spawn_time_green_ships,stage, pause_duration)
        last_asteroid_spawn_time = SpawnSystem.spawn_asteroids(enemy_ships, asteroid_spawn_rate, last_asteroid_spawn_time,stage, pause_duration)
        last_spawn_time_orange_ships = SpawnSystem.spawn_orange_enemy_ships(enemy_ships,orange_ship_spawn_rate,last_spawn_time_orange_ships,stage, pause_duration)

        return last_spawn_time_green_ships, last_asteroid_spawn_time, last_spawn_time_orange_ships
    elif stage == 3:

        last_spawn_time_orange_ships = SpawnSystem.spawn_orange_enemy_ships(enemy_ships,orange_ship_spawn_rate,last_spawn_time_orange_ships,stage, pause_duration)

        return last_spawn_time_green_ships, last_asteroid_spawn_time, last_spawn_time_orange_ships
    elif stage == 4:
        last_spawn_time_orange_ships = SpawnSystem.spawn_orange_enemy_ships(enemy_ships,orange_ship_spawn_rate,last_spawn_time_orange_ships,stage, pause_duration)

        return last_spawn_time_green_ships, last_asteroid_spawn_time, last_spawn_time_orange_ships
    elif stage == 5:
        last_spawn_time_orange_ships = SpawnSystem.spawn_orange_enemy_ships(enemy_ships,orange_ship_spawn_rate,last_spawn_time_orange_ships,stage, pause_duration)

        return last_spawn_time_green_ships, last_asteroid_spawn_time, last_spawn_time_orange_ships
    elif stage == 6:
        last_spawn_time_orange_ships = SpawnSystem.spawn_orange_enemy_ships(enemy_ships,orange_ship_spawn_rate,last_spawn_time_orange_ships,stage, pause_duration)

        return last_spawn_time_green_ships, last_asteroid_spawn_time, last_spawn_time_orange_ships
    elif stage == 7:#boss level
        last_spawn_time_orange_ships = SpawnSystem.spawn_orange_enemy_ships(enemy_ships,orange_ship_spawn_rate,last_spawn_time_orange_ships,stage, pause_duration)

        return last_spawn_time_green_ships, last_asteroid_spawn_time, last_spawn_time_orange_ships
    elif stage == 8: #tutorial level
        last_asteroid_spawn_time = SpawnSystem.spawn_asteroids(enemy_ships, asteroid_spawn_rate, last_asteroid_spawn_time,stage, pause_duration)


        return last_spawn_time_green_ships, last_asteroid_spawn_time, last_spawn_time_orange_ships



        




class SpawnSystem:
    def spawn_enemy_ships(entities, spawn_rate, last_spawn_time, stage, pause_duration):
        current_time = pygame.time.get_ticks() - pause_duration

        if stage == 1 and current_time - last_spawn_time > spawn_rate:
            num_ships = random.randint(green_ship_min_stage_1, green_ship_max_stage_1)
            for _ in range(num_ships):
                new_enemy_ship = ShipCreation.create_enemy_ship()
                entities.append(new_enemy_ship)

            last_spawn_time = current_time

        elif stage == 2 and current_time - last_spawn_time > spawn_rate:
            num_ships = random.randint(green_ship_min_stage_2, green_ship_max_stage_2)
            for _ in range(num_ships):
                new_enemy_ship = ShipCreation.create_enemy_ship()
                entities.append(new_enemy_ship)

            last_spawn_time = current_time

        return last_spawn_time
    
    def spawn_orange_enemy_ships(entities, spawn_rate, last_spawn_time, stage, pause_duration):
        current_time = pygame.time.get_ticks() - pause_duration

        if stage == 1 and current_time - last_spawn_time > spawn_rate:
            num_ships = random.randint(orange_min_stage_1, orange_max_stage_2)
            for _ in range(num_ships):
                new_enemy_ship = ShipCreation.create_orange_enemy_ship()
                entities.append(new_enemy_ship)

            last_spawn_time = current_time

        elif stage == 2 and current_time - last_spawn_time > spawn_rate:
            num_ships = random.randint(orange_min_stage_2, orange_max_stage_2)
            for _ in range(num_ships):
                new_enemy_ship = ShipCreation.create_orange_enemy_ship()
                entities.append(new_enemy_ship)

            last_spawn_time = current_time

        return last_spawn_time

    def spawn_asteroids(entities, spawn_rate, last_spawn_time, stage, pause_duration):
        current_time = pygame.time.get_ticks() - pause_duration

        if stage == 1 and current_time - last_spawn_time > spawn_rate:
            num_asteroids = random.randint(asteroid_min_stage_1, asteroid_max_stage_1)
            for _ in range(num_asteroids):
                asteroid = ShipCreation.create_asteroid()
                entities.append(asteroid)

            last_spawn_time = current_time

        elif stage == 2 and current_time - last_spawn_time > spawn_rate:
            num_asteroids = random.randint(asteroid_min_stage_2, asteroid_max_stage_2)
            for _ in range(num_asteroids):
                asteroid = ShipCreation.create_asteroid()
                entities.append(asteroid)

            last_spawn_time = current_time


        elif stage == 8 and current_time - last_spawn_time > spawn_rate:
            num_asteroids = random.randint(asteroid_min_stage_8, asteroid_max_stage_8)
            for _ in range(num_asteroids):
                asteroid = ShipCreation.create_asteroid()
                entities.append(asteroid)

            last_spawn_time = current_time

        return last_spawn_time