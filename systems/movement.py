import pygame
import config

maximum_y_value = config.DISPLAY_HEIGHT - 25
minimum_y_value = config.DISPLAY_HEIGHT - maximum_y_value

class MovementSystem:

    
    @staticmethod
    def move_player1(yellow_ship, keys_pressed, vel, spaceship_width,spaceship_height,dt):
        if yellow_ship.alive:
            # Access attributes and methods of the yellow_ship object directly
            if keys_pressed[pygame.K_w] and yellow_ship.position.y > 0:  # UP
                yellow_ship.position.y -= vel * dt
            if keys_pressed[pygame.K_s] and yellow_ship.position.y < config.DISPLAY_HEIGHT-spaceship_height:  # DOWN
                yellow_ship.position.y += vel * dt
            if keys_pressed[pygame.K_a] and yellow_ship.position.x > 0:  # LEFT
                yellow_ship.position.x -= vel * dt
            if keys_pressed[pygame.K_d] and yellow_ship.position.x < config.DISPLAY_WIDTH-spaceship_width:  # RIGHT
                yellow_ship.position.x += vel * dt
        
   
    @staticmethod
    def move_player2(red_ship, keys_pressed, vel, spaceship_width, spaceship_height, dt):
        if red_ship.alive:
        # Access attributes and methods of red ship object directly
            if keys_pressed[pygame.K_i] and red_ship.position.y > 0:  # UP 
                red_ship.position.y -= vel * dt
            if keys_pressed[pygame.K_k] and red_ship.position.y < config.DISPLAY_HEIGHT - spaceship_height:  # DOWN 
                red_ship.position.y += vel * dt
            if keys_pressed[pygame.K_j] and red_ship.position.x > 0:  # LEFT 
                red_ship.position.x -= vel * dt
            if keys_pressed[pygame.K_l] and red_ship.position.x < config.DISPLAY_WIDTH - spaceship_width:  # RIGHT 
                red_ship.position.x += vel * dt

    @staticmethod
    def move_enemy_ships(entities, dt):
        for entity in entities:
            if hasattr(entity, 'position'):
                if hasattr(entity, 'ship_color'):
                    if entity.ship_color == 'green':
                        entity.position.x -= entity.velocity * dt # Move green enemy ship with attribute velocity
                    elif entity.ship_color == 'grey':
                        entity.position.x -= entity.velocity * dt
                    elif entity.ship_color == 'orange':
                        entity.position.x -= entity.velocity * dt  # Move orange enemy ship with attribute velocity
                    elif entity.ship_color == 'purple':
                        entity.position.x -= entity.velocity * dt  # Move orange enemy ship with attribute velocity
                    elif entity.ship_color == 'blue':
                        entity.position.x -= entity.velocity * dt  # Move orange enemy ship with attribute velocity
                    elif entity.ship_color == 'brown':
                        entity.position.x -= entity.velocity * dt # Move orange enemy ship with attribute velocity
                    elif entity.ship_color == 'white':
                        entity.position.x -= entity.velocity * dt  # Move orange enemy ship with attribute velocity
                        if entity.position.x < config.DISPLAY_WIDTH - (config.DISPLAY_WIDTH/4):  # Check if boss ship has reached the desired width
                            entity.velocity = 0

                else:
                    entity.position.x -= entity.velocity * dt  # Move other enemy ships with default

                if entity.position.x < -config.DISPLAY_WIDTH:
                    entity.stop_moving()
                    entity.alive = False
                    entity.position.x = config.DISPLAY_WIDTH
                    entity.position.y = config.DISPLAY_HEIGHT
    

    
        
        
        


  
   