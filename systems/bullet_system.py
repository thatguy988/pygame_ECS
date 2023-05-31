import pygame
from components.bullet import Bullet

from components.dimension import Dimensions
import time
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

class BulletSystem:
    def __init__(self):
        self.bullets = []

    def create_bullet(self, x, y, velocity, radius):
        bullet = Bullet(x, y, velocity, radius)
        self.bullets.append(bullet)

    def fire_bullet(self, yellow, red, player_count, last_bullet_time, last_bullet_time_2):
        if player_count >= 1:
            bullet_pressed = pygame.key.get_pressed()[pygame.K_SPACE]
            if bullet_pressed:
                current_time = pygame.time.get_ticks()
                time_since_last_bullet = current_time - last_bullet_time

                if time_since_last_bullet >= 300: #millisecond delay
                    self.create_bullet(
                        yellow.position.x + SPACESHIP_WIDTH, yellow.position.y + SPACESHIP_HEIGHT // 2, 5, 10
                    )
                    last_bullet_time = current_time

        if player_count == 2:
            bullet_pressed_2 = pygame.key.get_pressed()[pygame.K_RETURN]
            if bullet_pressed_2:
                current_time_2 = pygame.time.get_ticks()
                time_since_last_bullet_2 = current_time_2 - last_bullet_time_2

                if time_since_last_bullet_2 >= 300:
                    self.create_bullet(
                        red.position.x + SPACESHIP_WIDTH, red.position.y + SPACESHIP_HEIGHT // 2, 5, 10        
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

            pygame.draw.rect(surface, color, (bullet.x, bullet.y, 5, 5))

    def update(self, width, color, surface):
        self.move_bullets()
        self.remove_offscreen_bullets(width)
        self.render_bullets(surface, color)



    def auto_fire(self, enemy_ship, velocity, radius, delay):
        current_time = time.time()
        last_fire_times = {}  # Dictionary to store the last fire time for each entity

        
        last_fire_time = last_fire_times.get(enemy_ship, delay)
        if current_time - last_fire_time >= delay:
            x = enemy_ship.position.x - 25  # Adjust the position as needed
            y = enemy_ship.position.y + SPACESHIP_HEIGHT // 2  # Adjust the position as needed
            self.create_bullet(x, y, velocity, radius)
            last_fire_times[enemy_ship] = current_time

    



    def update_bullets_and_check_collisions(self, enemy_ship, WIDTH, yellow, red, player_count, WIN, BLACK, HEIGHT):
        # Update bullets and check for collisions
        for bullet in self.bullets:
            bullet.update(WIDTH)
            
            # Check collision with yellow spaceship
            if yellow.position.x < bullet.x + bullet.radius < yellow.position.x + SPACESHIP_WIDTH:
                if yellow.position.y < bullet.y < yellow.position.y + SPACESHIP_HEIGHT:
                    # Collision detected with yellow spaceship
                    yellow.health -= 1
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
                        red.health -= 10
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
            if enemy_ship != self:  # Skip collision check with self


                if enemy_ship.position.x < bullet.x + bullet.radius < enemy_ship.position.x + SPACESHIP_WIDTH:
                    if enemy_ship.position.y < bullet.y < enemy_ship.position.y + SPACESHIP_HEIGHT:
                        # Collision detected with enemy spaceship
                        enemy_ship.health -= 10
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

'''
    def auto_fire(self, entities, velocity, radius, delay):
        current_time = time.time()
        last_fire_times = {}  # Dictionary to store the last fire time for each entity

        for entity in entities:
            last_fire_time = last_fire_times.get(entity, 600)
            if current_time - last_fire_time >= delay:
                x = entity.position.x  # Adjust the position as needed
                y = entity.position.y + SPACESHIP_HEIGHT // 2  # Adjust the position as needed
                self.create_bullet(x, y, velocity, radius)
                last_fire_times[entity] = current_time
'''


        
