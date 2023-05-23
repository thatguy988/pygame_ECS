import pygame
import random




class MovementSystem:
    @staticmethod
    
    def move_player1(yellow_ship, keys_pressed, width, height, vel, spaceship_width,spaceship_height):
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
        # Access attributes and methods of red ship object directly
            if keys_pressed[pygame.K_i] and red_ship.position.y > 0:  # UP 
                red_ship.position.y -= vel
            if keys_pressed[pygame.K_k] and red_ship.position.y < height - spaceship_height:  # DOWN 
                red_ship.position.y += vel
            if keys_pressed[pygame.K_j] and red_ship.position.x > 0:  # LEFT 
                red_ship.position.x -= vel
            if keys_pressed[pygame.K_l] and red_ship.position.x < width - spaceship_width:  # RIGHT 
                red_ship.position.x += vel


    @staticmethod
    def move_enemy_ships(entities, width, vel):
        for entity in entities:
            if hasattr(entity, 'position'):
                entity.position.x -= vel  # Move the enemy ship to the left

                if entity.position.x < -width:
                    # Enemy ship reached the left side, generate a new random y-axis position
                    entity.position.x = width  # Reset x-coordinate to the right side
                    entity.position.y = random.randint(25, 475)  # Generate a new random y-coordinate


  
   