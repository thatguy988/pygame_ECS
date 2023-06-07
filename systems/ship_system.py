import pygame
import random

from components.ship import ShipCreation



# Spawn rates for different enemy ships and asteroids
spawn_rates = {
    "green": 8000,
    "orange": 5000,
    "purple": 500,
    "blue": 4000,
    "brown": 3000,
    "grey": 3000,
}

# Minimum and maximum numbers of ships for different stages
ship_numbers = {
    "green": {
        1: (1, 2),
        2: (1, 2),
    },
    "orange": {
        1: (0, 2),
        2: (0, 2),
        3: (0, 1),
        4: (1, 2),
        5: (1, 2),
        6: (1, 2),
    },
    "purple": {
        3: (1, 3),
        4: (1, 3),
        5: (1, 3),
        6: (1, 3),
    },
    "blue": {
        4: (1, 3),
        5: (1, 3),
        6: (1, 3),
    },
    "brown": {
        5: (1, 3),
        6: (1, 3),
    },
    "grey": {
        1: (1, 2),
        2: (0, 1),
        8: (1, 2),
    },
}

# Accessing spawn rates
green_ship_spawn_rate = spawn_rates["green"]  # Returns 5000
orange_ship_spawn_rate = spawn_rates["orange"]  # Returns 1000
purple_ship_spawn_rate = spawn_rates["purple"]  # Returns 2000
blue_ship_spawn_rate = spawn_rates["blue"]  # Returns 4000
brown_ship_spawn_rate = spawn_rates["brown"]  # Returns 3000
grey_spawn_rate = spawn_rates["grey"]  # Returns 3000

# Accessing ship numbers
green_ship_numbers = ship_numbers["green"]
orange_ship_numbers = ship_numbers["orange"]
purple_ship_numbers = ship_numbers["purple"]
blue_ship_numbers = ship_numbers["blue"]
brown_ship_numbers = ship_numbers["brown"]
grey_ship_numbers = ship_numbers["grey"]

# Green ships
green_ship_stage_1_min, green_ship_stage_1_max = ship_numbers["green"][1]
green_ship_stage_2_min, green_ship_stage_2_max = ship_numbers["green"][2]

# Orange ships
orange_ship_stage_1_min, orange_ship_stage_1_max = ship_numbers["orange"][1]
orange_ship_stage_2_min, orange_ship_stage_2_max = ship_numbers["orange"][2]
orange_ship_stage_3_min, orange_ship_stage_3_max = ship_numbers["orange"][3]
orange_ship_stage_4_min, orange_ship_stage_4_max = ship_numbers["orange"][4]
orange_ship_stage_5_min, orange_ship_stage_5_max = ship_numbers["orange"][5]
orange_ship_stage_6_min, orange_ship_stage_6_max = ship_numbers["orange"][6]

# Purple ships
purple_ship_stage_3_min, purple_ship_stage_3_max = ship_numbers["purple"][3]
purple_ship_stage_4_min, purple_ship_stage_4_max = ship_numbers["purple"][4]
purple_ship_stage_5_min, purple_ship_stage_5_max = ship_numbers["purple"][5]
purple_ship_stage_6_min, purple_ship_stage_6_max = ship_numbers["purple"][6]

# Blue ships
blue_ship_stage_4_min, blue_ship_stage_4_max = ship_numbers["blue"][4]
blue_ship_stage_5_min, blue_ship_stage_5_max = ship_numbers["blue"][5]
blue_ship_stage_6_min, blue_ship_stage_6_max = ship_numbers["blue"][6]

# Brown ships
brown_ship_stage_5_min, brown_ship_stage_5_max = ship_numbers["brown"][5]
brown_ship_stage_6_min, brown_ship_stage_6_max = ship_numbers["brown"][6]

# Grey ships
grey_ship_stage_1_min, grey_ship_stage_1_max = ship_numbers["grey"][1]
grey_ship_stage_2_min, grey_ship_stage_2_max = ship_numbers["grey"][2]
grey_ship_stage_8_min, grey_ship_stage_8_max = ship_numbers["grey"][8]




def create_ships(enemy_ships, pause_duration, stage, *args):
    last_spawn_times = []
    print(f"Args: {args}")

    
    if stage in green_ship_numbers:
        last_spawn_time_green_ships = SpawnSystem.spawn_green_enemy_ships(enemy_ships, green_ship_spawn_rate, args[0], stage, pause_duration)
        last_spawn_times.append(last_spawn_time_green_ships)
        print(last_spawn_times)

        
    if stage in ship_numbers["orange"]:
        last_spawn_time_orange_ships = SpawnSystem.spawn_orange_enemy_ships(enemy_ships, orange_ship_spawn_rate, args[2], stage, pause_duration)
        last_spawn_times.append(last_spawn_time_orange_ships)
        print(last_spawn_times)
 
    if stage in ship_numbers["purple"]:
        last_spawn_time_purple_ships = SpawnSystem.spawn_purple_enemy_ships(enemy_ships, purple_ship_spawn_rate, args[3], stage, pause_duration)
        last_spawn_times.append(last_spawn_time_purple_ships)
        print(last_spawn_times)

    if stage in ship_numbers["blue"]:
        last_spawn_time_blue_ships = SpawnSystem.spawn_blue_enemy_ships(enemy_ships, blue_ship_spawn_rate, args[4], stage, pause_duration)
        last_spawn_times.append(last_spawn_time_blue_ships)
        print(last_spawn_times)

    if stage in ship_numbers["brown"]:
        last_spawn_time_brown_ships = SpawnSystem.spawn_brown_enemy_ships(enemy_ships, brown_ship_spawn_rate, args[5], stage, pause_duration)
        last_spawn_times.append(last_spawn_time_brown_ships)
        print(last_spawn_times)

    if stage in ship_numbers["grey"]:
        last_asteroid_spawn_time = SpawnSystem.spawn_asteroids(enemy_ships, grey_spawn_rate, args[1], stage, pause_duration)
        last_spawn_times.append(last_asteroid_spawn_time)
        print(last_spawn_times)


    return tuple(last_spawn_times)

   
class SpawnSystem:
    def spawn_green_enemy_ships(entities, spawn_rate, last_spawn_time, stage, pause_duration):
        current_time = pygame.time.get_ticks() - pause_duration

        if stage == 1 and current_time - last_spawn_time > spawn_rate:
            num_ships = random.randint(green_ship_stage_1_min, green_ship_stage_1_max)
            for _ in range(num_ships):
                new_enemy_ship = ShipCreation.create_green_enemy_ship()
                entities.append(new_enemy_ship)

            last_spawn_time = current_time

        elif stage == 2 and current_time - last_spawn_time > spawn_rate:
            num_ships = random.randint(green_ship_stage_2_min, green_ship_stage_2_max)
            for _ in range(num_ships):
                new_enemy_ship = ShipCreation.create_green_enemy_ship()
                entities.append(new_enemy_ship)

            last_spawn_time = current_time

        return last_spawn_time
    
    def spawn_orange_enemy_ships(entities, spawn_rate, last_spawn_time, stage, pause_duration):
        current_time = pygame.time.get_ticks() - pause_duration

        if stage >= 1 and stage != 7 and current_time - last_spawn_time > spawn_rate:
            if stage == 1:
                num_ships = random.randint(orange_ship_stage_2_min, orange_ship_stage_2_max)
            elif stage == 3:
                num_ships = random.randint(orange_ship_stage_3_min, orange_ship_stage_3_max)
            elif stage == 4:
                num_ships = random.randint(orange_min_stage_4, orange_max_stage_4)
            elif stage == 5:
                num_ships = random.randint(orange_min_stage_4, orange_max_stage_4)
            elif stage == 6:
                num_ships = random.randint(orange_min_stage_5, orange_max_stage_5)
            for _ in range(num_ships):
                new_enemy_ship = ShipCreation.create_orange_enemy_ship()
                entities.append(new_enemy_ship)

            last_spawn_time = current_time

        return last_spawn_time
    
    def spawn_purple_enemy_ships(entities, spawn_rate, last_spawn_time, stage, pause_duration):
        current_time = pygame.time.get_ticks() - pause_duration

        if stage >= 3 and stage != 7 and current_time - last_spawn_time > spawn_rate:
            if stage == 3:
                num_ships = random.randint(purple_ship_stage_3_min, purple_ship_stage_3_max)
            elif stage == 4:
                num_ships = random.randint(purple_min_stage_3, purple_max_stage_3)
            elif stage == 5:
                num_ships = random.randint(purple_min_stage_3, purple_max_stage_3)
            elif stage == 6:
                num_ships = random.randint(purple_min_stage_3, purple_max_stage_3)
            for _ in range(num_ships):
                new_enemy_ship = ShipCreation.create_orange_enemy_ship()
                entities.append(new_enemy_ship)

            last_spawn_time = current_time
        return last_spawn_time
    
    def spawn_blue_enemy_ships(entities, spawn_rate, last_spawn_time, stage, pause_duration):
        current_time = pygame.time.get_ticks() - pause_duration
        if stage >= 4 and stage != 7 and current_time - last_spawn_time > spawn_rate:
            if stage == 4:
                num_ships = random.randint(purple_min_stage_3, purple_max_stage_3)
            elif stage == 5:
                num_ships = random.randint(purple_min_stage_3, purple_max_stage_3)
            elif stage == 6:
                num_ships = random.randint(purple_min_stage_3, purple_max_stage_3)
            for _ in range(num_ships):
                new_enemy_ship = ShipCreation.create_orange_enemy_ship()
                entities.append(new_enemy_ship)

            last_spawn_time = current_time
        return last_spawn_time

        
    
    def spawn_brown_enemy_ships(entities, spawn_rate, last_spawn_time, stage, pause_duration):
        current_time = pygame.time.get_ticks() - pause_duration
        if stage >= 5 and stage != 7 and current_time - last_spawn_time > spawn_rate:
            if stage == 5:
                num_ships = random.randint(purple_min_stage_3, purple_max_stage_3)
            elif stage == 6:
                num_ships = random.randint(purple_min_stage_3, purple_max_stage_3)
            for _ in range(num_ships):
                new_enemy_ship = ShipCreation.create_orange_enemy_ship()
                entities.append(new_enemy_ship)

            last_spawn_time = current_time
        return last_spawn_time

        

    def spawn_asteroids(entities, spawn_rate, last_spawn_time, stage, pause_duration):
        current_time = pygame.time.get_ticks() - pause_duration

        if stage == 1 and current_time - last_spawn_time > spawn_rate:
            num_ships = random.randint(grey_ship_stage_1_min, grey_ship_stage_1_max)
            for _ in range(num_ships):
                new_enemy_ship = ShipCreation.create_asteroid()
                entities.append(new_enemy_ship)

            last_spawn_time = current_time


        return last_spawn_time