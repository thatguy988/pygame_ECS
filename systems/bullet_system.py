import pygame
from components.bullet import Bullet

from components.dimension import Dimensions
import time
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

class BulletSystem:
    def __init__(self):
        self.bullets = []
        self.last_fire_times = {}  # Dictionary to store the last fire time for each entity


    def create_bullet(self, x, y, velocity, radius, owner):
        bullet = Bullet(x, y, velocity, radius, owner)
        self.bullets.append(bullet)

    def fire_bullet(self, yellow, red, player_count, last_bullet_time, last_bullet_time_2):
        if player_count >= 1:
            bullet_pressed = pygame.key.get_pressed()[pygame.K_SPACE]
            if bullet_pressed:
                current_time = pygame.time.get_ticks()
                time_since_last_bullet = current_time - last_bullet_time

                if time_since_last_bullet >= 300: #millisecond delay
                    self.create_bullet(
                        yellow.position.x + SPACESHIP_WIDTH, yellow.position.y + SPACESHIP_HEIGHT // 2, 5, 10, "yellow"
                    )
                    last_bullet_time = current_time

        if player_count == 2:
            bullet_pressed_2 = pygame.key.get_pressed()[pygame.K_RETURN]
            if bullet_pressed_2:
                current_time_2 = pygame.time.get_ticks()
                time_since_last_bullet_2 = current_time_2 - last_bullet_time_2

                if time_since_last_bullet_2 >= 300:
                    self.create_bullet(
                        red.position.x + SPACESHIP_WIDTH, red.position.y + SPACESHIP_HEIGHT // 2, 5, 10 , "red"       
                    )
                    last_bullet_time_2 = current_time_2
        return last_bullet_time, last_bullet_time_2
    

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.x += bullet.velocity

    def remove_bullet(self, bullet):
        self.bullets.remove(bullet)
        

    def remove_offscreen_bullets(self, width):
        self.bullets = [bullet for bullet in self.bullets if bullet.x < width]


    def render_bullets(self, surface, color):
        for bullet in self.bullets:
            if bullet.owner == "yellow":
                bullet_color = (255, 255, 0)  # Yellow color
            elif bullet.owner == "red":
                bullet_color = (255, 0, 0)  # Red color
            elif bullet.owner == "green":
                bullet_color = (0,255,0) #green color
            else:
                bullet_color = (255, 255, 255)  # Default color (white)

            pygame.draw.rect(surface, bullet_color, (bullet.x, bullet.y, 5, 5))

    


    def update(self, width, color, surface):
        self.move_bullets()
        self.remove_offscreen_bullets(width)
        self.render_bullets(surface, color)

    


    def auto_fire(self, enemy_ship, last_bullet_time_enemy_ship):
        delay = 1200
        current_time = pygame.time.get_ticks()
        time_since_last_bullet = current_time - last_bullet_time_enemy_ship

        if time_since_last_bullet >= delay: #millisecond delay
            self.create_bullet(
                enemy_ship.position.x - 1, enemy_ship.position.y + SPACESHIP_HEIGHT // 2, -5, 10, "green"
            )
            last_bullet_time_enemy_ship = current_time

        return last_bullet_time_enemy_ship


    
    



    def update_bullets_and_check_collisions(self, enemy_ship, WIDTH, yellow, red, player_count, WIN, BLACK, HEIGHT):
        # Update bullets and check for collisions
        bullet_damage = 5
        for bullet in self.bullets:
            bullet.update(WIDTH)
            
            # Check collision with yellow spaceship
            if yellow.position.x < bullet.x + bullet.radius < yellow.position.x + SPACESHIP_WIDTH:
                if yellow.position.y < bullet.y < yellow.position.y + SPACESHIP_HEIGHT:
                    # Collision detected with yellow spaceship
                    yellow.health -= bullet_damage
                    self.remove_bullet(bullet)

                    # Check if yellow spaceship's health reaches zero
                    if yellow.health <= 0:
                        yellow.health = 0
                        yellow.alive = False
                        yellow.stop_moving()
                    
                        yellow.visible = False

                    
            
            # Check collision with red spaceship
            if player_count == 2:
                if red.position.x < bullet.x + bullet.radius < red.position.x + SPACESHIP_WIDTH:
                    if red.position.y < bullet.y < red.position.y + SPACESHIP_HEIGHT:
                        # Collision detected with red spaceship
                        red.health -= bullet_damage
                        self.remove_bullet(bullet)

                        # Check if red spaceship's health reaches zero
                        if red.health <= 0:
                            red.health = 0
                            red.alive = False
                            red.visible = False
                            red.stop_moving()

                        
            # Check collision with enemy spaceship
        #for enemy_ship in entities:
            #for bullet in self.bullets:
            


            if bullet.owner != "green":
                if enemy_ship.position.x < bullet.x + bullet.radius < enemy_ship.position.x + SPACESHIP_WIDTH:
                    if enemy_ship.position.y < bullet.y < enemy_ship.position.y + SPACESHIP_HEIGHT:
                        # Collision detected with enemy spaceship
                        enemy_ship.health -= bullet_damage
                        self.remove_bullet(bullet)

                        # Check if enemy spaceship's health reaches zero
                        if enemy_ship.health <= 0:
                            enemy_ship.stop_moving()
                            enemy_ship.visible = False

                            enemy_ship.position.x = WIDTH
                            enemy_ship.position.y = HEIGHT
                            enemy_ship.health = 10
                            enemy_ship.visible = True

        self.update(WIDTH, BLACK, WIN)









        
