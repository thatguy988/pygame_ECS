import pygame
import random

from components.ship import ShipCreation



# Spawn rates for different enemy ships and asteroids
spawn_rates = {
    "green": 3000,
    "orange": 5000,
    "purple": 7000,
    "blue": 6000,
    "brown": 9000,
    "grey": 3000,
}

# Minimum and maximum numbers of ships for different stages
ship_numbers = {
    "green": {
        1: (0, 4),
        2: (0, 4),
        3: (0, 1),
    },
    "orange": {
        2: (1, 3),
        3: (1, 3),
        4: (2, 4),
        5: (1, 2),
    },
    "purple": {
        3: (2, 4),
        4: (2, 3),
        5: (2, 3),
        6: (2, 3),
    },
    "blue": {
        4: (1, 3),
        5: (1, 3),
        6: (1, 3),
    },
    "brown": {
        5: (2, 4),
        6: (2, 5),
    },
    "grey": {
        0: (1, 2),
        1: (1, 2),
        8: (1, 2),
    },
}

# access spawn rate
spawn_rate_dict = {key: spawn_rates[key] for key in spawn_rates}

# access ship numbers
ship_numbers_dict = {
    ship_type: {key: ship_numbers[ship_type][key] for key in ship_numbers[ship_type]}
    for ship_type in ship_numbers
}




def create_ships(enemy_ships, pause_duration, game_start_time, stage, *args):
    last_spawn_times = []
    #print(f"Args: {args}")

    
    if stage in ship_numbers_dict["green"]:
        last_spawn_time_green_ships = SpawnSystem.spawn_green_enemy_ships(enemy_ships, args[0], stage, pause_duration, game_start_time)
        last_spawn_times.append(last_spawn_time_green_ships)
        #print(last_spawn_times)
    

    if stage in ship_numbers_dict["grey"]:
        last_asteroid_spawn_time = SpawnSystem.spawn_asteroids(enemy_ships, args[1], stage, pause_duration, game_start_time)
        last_spawn_times.append(last_asteroid_spawn_time)

        
    if stage in ship_numbers_dict["orange"]:
        last_spawn_time_orange_ships = SpawnSystem.spawn_orange_enemy_ships(enemy_ships, args[2], stage, pause_duration, game_start_time)
        last_spawn_times.append(last_spawn_time_orange_ships)
        #print(last_spawn_times)
 
    if stage in ship_numbers_dict["purple"]:
        last_spawn_time_purple_ships = SpawnSystem.spawn_purple_enemy_ships(enemy_ships, args[3], stage, pause_duration, game_start_time)
        last_spawn_times.append(last_spawn_time_purple_ships)
        #print(last_spawn_times)

    if stage in ship_numbers_dict["blue"]:
        last_spawn_time_blue_ships = SpawnSystem.spawn_blue_enemy_ships(enemy_ships, args[4], stage, pause_duration, game_start_time)
        last_spawn_times.append(last_spawn_time_blue_ships)
        #print(last_spawn_times)

    if stage in ship_numbers_dict["brown"]:
        last_spawn_time_brown_ships = SpawnSystem.spawn_brown_enemy_ships(enemy_ships, args[5], stage, pause_duration, game_start_time)
        last_spawn_times.append(last_spawn_time_brown_ships)
        #print(last_spawn_times)



    return tuple(last_spawn_times)



class SpawnSystem:
    @staticmethod
    def spawn_ship(entities, last_spawn_time, stage, pause_duration, game_start_time, ship_creation_func, ship_type):
        current_time = pygame.time.get_ticks() - pause_duration - game_start_time
        if stage in ship_numbers_dict[ship_type] and current_time - last_spawn_time > spawn_rate_dict[ship_type]:
            min_ships, max_ships = ship_numbers_dict[ship_type][stage]
            num_ships = random.randint(min_ships, max_ships)
            for _ in range(num_ships):
                new_enemy_ship = ship_creation_func()
                entities.append(new_enemy_ship)
            last_spawn_time = current_time
        return last_spawn_time

    @staticmethod
    def spawn_green_enemy_ships(entities, last_spawn_time, stage, pause_duration, game_start_time):
        return SpawnSystem.spawn_ship(entities, last_spawn_time, stage, pause_duration, game_start_time, ShipCreation.create_green_enemy_ship, "green")

    @staticmethod
    def spawn_orange_enemy_ships(entities, last_spawn_time, stage, pause_duration, game_start_time):
        return SpawnSystem.spawn_ship(entities, last_spawn_time, stage, pause_duration, game_start_time, ShipCreation.create_orange_enemy_ship, "orange")

    @staticmethod
    def spawn_purple_enemy_ships(entities, last_spawn_time, stage, pause_duration, game_start_time):
        return SpawnSystem.spawn_ship(entities, last_spawn_time, stage, pause_duration, game_start_time, ShipCreation.create_purple_enemy_ship, "purple")

    @staticmethod
    def spawn_blue_enemy_ships(entities, last_spawn_time, stage, pause_duration, game_start_time):
        return SpawnSystem.spawn_ship(entities, last_spawn_time, stage, pause_duration, game_start_time, ShipCreation.create_blue_enemy_ship, "blue")

    @staticmethod
    def spawn_brown_enemy_ships(entities, last_spawn_time, stage, pause_duration, game_start_time):
        return SpawnSystem.spawn_ship(entities, last_spawn_time, stage, pause_duration, game_start_time, ShipCreation.create_brown_enemy_ship, "brown")

    @staticmethod
    def spawn_asteroids(entities, last_spawn_time, stage, pause_duration, game_start_time):
        return SpawnSystem.spawn_ship(entities, last_spawn_time, stage, pause_duration, game_start_time, ShipCreation.create_asteroid, "grey")
