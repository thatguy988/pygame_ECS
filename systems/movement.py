import pygame
import random


class MovementSystem:

    
    @staticmethod
    def move_player1(yellow_ship, keys_pressed, width, height, vel, spaceship_width,spaceship_height):
        if yellow_ship.alive:
            # Access attributes and methods of the yellow_ship object directly
            if keys_pressed[pygame.K_w] and yellow_ship.position.y > 0:  # UP
                yellow_ship.position.y -= vel
            if keys_pressed[pygame.K_s] and yellow_ship.position.y < height-spaceship_height:  # DOWN
                yellow_ship.position.y += vel
            if keys_pressed[pygame.K_a] and yellow_ship.position.x > 0:  # LEFT
                yellow_ship.position.x -= vel
            if keys_pressed[pygame.K_d] and yellow_ship.position.x < width-spaceship_width:  # RIGHT
                yellow_ship.position.x += vel
        
   
    @staticmethod
    def move_player2(red_ship, keys_pressed, width, height, vel, spaceship_width, spaceship_height):
        if red_ship.alive:
        # Access attributes and methods of red ship object directly
            if keys_pressed[pygame.K_i] and red_ship.position.y > 0:  # UP 
                red_ship.position.y -= vel
            if keys_pressed[pygame.K_k] and red_ship.position.y < height - spaceship_height:  # DOWN 
                red_ship.position.y += vel
            if keys_pressed[pygame.K_j] and red_ship.position.x > 0:  # LEFT 
                red_ship.position.x -= vel
            if keys_pressed[pygame.K_l] and red_ship.position.x < width - spaceship_width:  # RIGHT 
                red_ship.position.x += vel

    '''
    @staticmethod
    def move_enemy_ships(entities, width, vel):
        for entity in entities:
            if hasattr(entity, 'position'):
                entity.position.x -= vel  # Move the enemy ship to the left

                if entity.position.x < -width:
                    # Enemy ship reached the left side, generate a new random y-axis position
                    entity.position.x = width  # Reset x-coordinate to the right side
                    entity.position.y = random.randint(25, 475)  # Generate a new random y-coordinate
    '''
    @staticmethod
    def move_enemy_ships(entities, width):
        for entity in entities:
            if hasattr(entity, 'position'):
                if hasattr(entity, 'ship_color'):
                    if entity.ship_color == 'green':
                        entity.position.x -= entity.velocity  # Move green enemy ship with its specific velocity
                    elif entity.ship_color == 'grey':
                        entity.position.x -= entity.velocity
                    elif entity.ship_color == 'orange':
                        entity.position.x -= entity.velocity  # Move orange enemy ship with its specific velocity
                else:
                    entity.position.x -= entity.velocity  # Move other enemy ships with their default velocity

                if entity.position.x < -width:
                    # Enemy ship reached the left side, generate a new random y-axis position
                    entity.position.x = width  # Reset x-coordinate to the right side
                    entity.position.y = random.randint(25, 475)  # Generate a new random y-coordinate

    
    @staticmethod           
    def move_asteroid(asteroids, width):
        for asteroid in asteroids:
            if hasattr(asteroid, 'position'):
                asteroid.position.x -= asteroid.velocity  # Move the enemy ship to the left

                if asteroid.position.x < -width:
                    # Enemy ship reached the left side, generate a new random y-axis position
                    asteroid.position.x = width  # Reset x-coordinate to the right side
                    asteroid.position.y = random.randint(25, 475)  # Generate a new random y-coordinate
    

    
        
        
        


  
   