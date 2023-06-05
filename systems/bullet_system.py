import pygame
import random
from components.bullet import Bullet
from components.score import Score
from components.explosion import Explosion, load_explosion_images


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)    
RED = (255, 0, 0)
GREEN = (0,255,0)
ORANGE = (255, 165, 0)
WIDTH, HEIGHT = 1400, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))



green_ship_points = 10
asteroid_points = 5



class BulletSystem:
    def __init__(self):
        self.bullets = []
        self.last_fire_times = {}  # Dictionary to store the last fire time for each entity


    def create_bullet(self, x, y, velocity, radius, owner):
        bullet = Bullet(x, y, velocity, radius, owner)
        self.bullets.append(bullet)

    def fire_bullet(self, yellow, red, player_count, last_bullet_time, last_bullet_time_2, pause_duration):
        player_bullet_delay = 300
        if player_count >= 1:
            if yellow.alive:
                bullet_pressed = pygame.key.get_pressed()[pygame.K_SPACE]
                if bullet_pressed:
                    current_time = pygame.time.get_ticks() - pause_duration
                    time_since_last_bullet = current_time - last_bullet_time

                    if time_since_last_bullet >= player_bullet_delay: #millisecond delay
                        self.create_bullet(
                            yellow.position.x + yellow.width, yellow.position.y + yellow.height // 2, 5, 10, "yellow"
                        )
                        last_bullet_time = current_time
            

        if player_count == 2:
            if red.alive:
                bullet_pressed_2 = pygame.key.get_pressed()[pygame.K_RETURN]
                if bullet_pressed_2:
                    current_time_2 = pygame.time.get_ticks() - pause_duration
                    time_since_last_bullet_2 = current_time_2 - last_bullet_time_2

                    if time_since_last_bullet_2 >= player_bullet_delay:
                        self.create_bullet(
                            red.position.x + red.width, red.position.y + red.height // 2, 5, 10 , "red"       
                        )
                        last_bullet_time_2 = current_time_2
        return last_bullet_time, last_bullet_time_2
    

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.x += bullet.velocity

    def remove_bullet(self, bullet):
        if bullet in self.bullets:
            self.bullets.remove(bullet)
        

    def remove_offscreen_bullets(self, width):
        self.bullets = [bullet for bullet in self.bullets if bullet.x < width]


    def render_bullets(self, surface, color):
        for bullet in self.bullets:
            if bullet.owner == "yellow":
                bullet_color = YELLOW  # Yellow color
            elif bullet.owner == "red":
                bullet_color = RED  # Red color
            elif bullet.owner == "green":
                bullet_color = GREEN #green color
            elif bullet.owner == "orange":
                bullet_color = ORANGE
            else:
                bullet_color = WHITE  # Default color (white)

            pygame.draw.rect(surface, bullet_color, (bullet.x, bullet.y, 5, 5))
        

    def update(self, width, color, surface):
        self.move_bullets()
        self.remove_offscreen_bullets(width)
        self.render_bullets(surface, color)

    
    def auto_fire(self, enemy_ships, last_bullet_time_green_ship, last_bullet_time_orange_ship, pause_duration):
        current_time = pygame.time.get_ticks() - pause_duration
        time_since_last_bullet_green = current_time - last_bullet_time_green_ship
        time_since_last_bullet_orange = current_time - last_bullet_time_orange_ship

        # Define the color-delay mapping
        color_delays = {
            "green": 2000,  # Delay for green enemy ships
            "orange": 1000,   # Delay for orange enemy ships
            
        }


        for enemy_ship in enemy_ships:
            if hasattr(enemy_ship, "ship_color") and enemy_ship.ship_color in color_delays:
                delay = color_delays[enemy_ship.ship_color]
                
                if enemy_ship.ship_color == "green" and time_since_last_bullet_green >=delay:
                        # Fire two bullets for green enemy ships
                    self.create_bullet(
                            enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2 - 10, -5, 10, "green"
                        )
                    self.create_bullet(
                            enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2 + 10, -5, 10, "green"
                        )
                    last_bullet_time_green_ship = current_time
                elif enemy_ship.ship_color == "orange" and time_since_last_bullet_orange>=delay:
                        # Fire a single bullet for orange enemy ships
                    self.create_bullet(
                            enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2, -5, 10, "orange"
                        )
                    last_bullet_time_orange_ship = current_time
                    # Break the loop if you want to fire bullets for only one enemy ship at a time
                    # break

        return last_bullet_time_green_ship, last_bullet_time_orange_ship
    
    
    
    def update_bullets_and_check_collisions(self, enemy_ships, WIDTH, yellow, red, player_count, background, HEIGHT, scoreboard, explosions):
        

        for bullet in self.bullets:
            bullet.update(WIDTH)
            if yellow.alive and yellow.visible:
                if bullet.owner != "red" and bullet.owner != "yellow":
                    if yellow.position.x < bullet.x + bullet.radius < yellow.position.x + yellow.width:
                        if yellow.position.y < bullet.y < yellow.position.y + yellow.height:
                            # Collision detected with yellow spaceship bullet from enemy ship
                            yellow.health -= enemy_ship.bullet_damage
                            self.remove_bullet(bullet)

                            # Check if yellow spaceship's health reaches zero
                            if yellow.health <= 0:
                                yellow.health = 0
                                yellow.alive = False
                                yellow.visible = False
                                

            if player_count == 2:
                if red.alive and red.visible:
                    if bullet.owner != "yellow" and bullet.owner != "red":
                        if red.position.x < bullet.x + bullet.radius < red.position.x + red.width:
                            if red.position.y < bullet.y < red.position.y + red.height:
                                # Collision detected with red spaceship
                                red.health -= enemy_ship.bullet_damage
                                self.remove_bullet(bullet)

                                # Check if red spaceship's health reaches zero
                                if red.health <= 0:
                                    red.health = 0
                                    red.alive = False
                                    red.visible = False
                                    

            for enemy_ship in enemy_ships:
                if bullet.owner != "green" and bullet.owner != "orange":
                    if enemy_ship.position.x < bullet.x + bullet.radius < enemy_ship.position.x + enemy_ship.width:
                        if enemy_ship.position.y < bullet.y < enemy_ship.position.y + enemy_ship.height:
                            # Collision detected with enemy spaceship
                            enemy_ship.health -= yellow.bullet_damage
                            self.remove_bullet(bullet)

                            # Check if enemy spaceship's health reaches zero
                            if enemy_ship.health <= 0:
                                # Create an explosion at (x, y) and add it to the list
                                explosion = Explosion(enemy_ship.position.x, enemy_ship.position.y)
                                enemy_rect = pygame.Rect(enemy_ship.position.x, enemy_ship.position.y, enemy_ship.width, enemy_ship.height)

                                explosions.append(explosion)

    
                                for explosion in explosions:
                                    explosion.update()
                                    explosion.draw(background)
                                    # Update the game display
                                    pygame.display.update(enemy_rect)

                                    
                                    
                                enemy_ship.stop_moving()
                                enemy_ship.visible = False
                                enemy_ship.position.x = WIDTH
                                enemy_ship.position.y = HEIGHT
                                
                            
                                enemy_ship.health = enemy_ship.initial_health
                                enemy_ship.visible = True
                                scoreboard.reward_points(enemy_ship.ship_color)

        
        
            
            
        

            


        

        


        
            
                                
                
               
    
    def handle_enemyship_ship_collision(self, ship, enemy_ships, WIDTH, HEIGHT,scoreboard):
        for enemy_ship in enemy_ships:
            if ship.alive and ship.visible and enemy_ship.alive and enemy_ship.visible:
                if ship.position.x < enemy_ship.position.x + enemy_ship.width and \
                        ship.position.x + ship.width > enemy_ship.position.x and \
                        ship.position.y < enemy_ship.position.y + enemy_ship.height and \
                        ship.position.y + ship.height > enemy_ship.position.y:
                    # Collision detected between yellow player ship and enemy ship
                    ship.health -= enemy_ship.collision_damage  # Reduce yellow player ship's health based on enemy ship's damage
                    enemy_ship.health -= ship.collision_damage  # Reduce enemy ship's health based on yellow player ship's damage

                    if ship.health <= 0:
                        ship.alive = False
                        ship.visible = False
                        # Handle yellow player ship's destruction

                    if enemy_ship.health <= 0:
                        
                        enemy_ship.stop_moving()
                        enemy_ship.visible = False

                        enemy_ship.position.x = WIDTH
                        enemy_ship.position.y = HEIGHT
                        enemy_ship.health = enemy_ship.initial_health
                        enemy_ship.visible = True
                        scoreboard.reward_points(enemy_ship.ship_color)





    

            






            
