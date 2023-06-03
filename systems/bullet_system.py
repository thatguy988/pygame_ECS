import pygame
import random
from components.bullet import Bullet
from components.score import Score

from components.dimension import Dimensions



class BulletSystem:
    def __init__(self):
        self.bullets = []
        self.last_fire_times = {}  # Dictionary to store the last fire time for each entity


    def create_bullet(self, x, y, velocity, radius, owner):
        bullet = Bullet(x, y, velocity, radius, owner)
        self.bullets.append(bullet)

    def fire_bullet(self, yellow, red, player_count, last_bullet_time, last_bullet_time_2, pause_duration):
        if player_count >= 1:
            if yellow.alive:
                bullet_pressed = pygame.key.get_pressed()[pygame.K_SPACE]
                if bullet_pressed:
                    current_time = pygame.time.get_ticks() - pause_duration
                    time_since_last_bullet = current_time - last_bullet_time

                    if time_since_last_bullet >= 300: #millisecond delay
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

                    if time_since_last_bullet_2 >= 300:
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

    #double bullets
    def auto_fire(self, enemy_ships, last_bullet_time_enemy_ship, pause_duration):
        delay = 3000
        current_time = pygame.time.get_ticks() - pause_duration
        time_since_last_bullet = current_time - last_bullet_time_enemy_ship

        if time_since_last_bullet >= delay:
            for enemy_ship in enemy_ships:
                self.create_bullet(
                    enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2 - 10, -5, 10, "green"
                )
                self.create_bullet(
                    enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2 + 10, -5, 10, "green"
                )
            last_bullet_time_enemy_ship = current_time

        return last_bullet_time_enemy_ship


    #single bullets
    '''
    def auto_fire(self, enemy_ships, last_bullet_time_enemy_ship,pause_duration):
        delay = 3000
        current_time = pygame.time.get_ticks() - pause_duration
        time_since_last_bullet = current_time - last_bullet_time_enemy_ship

        if time_since_last_bullet >= delay:  # millisecond delay
            for enemy_ship in enemy_ships:
                self.create_bullet(
                    enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2, -5, 10, "green"
                )
            last_bullet_time_enemy_ship = current_time

        return last_bullet_time_enemy_ship
    '''
    
    '''
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
    '''

    
    
    def update_bullets_and_check_collisions(self, enemy_ships, WIDTH, yellow, red, player_count, WIN, BLACK, HEIGHT, asteroids,scoreboard):
        bullet_damage = 5
        for bullet in self.bullets:
            bullet.update(WIDTH)
            if yellow.alive and yellow.visible:
                if bullet.owner != "red" and bullet.owner != "yellow":
                    if yellow.position.x < bullet.x + bullet.radius < yellow.position.x + yellow.width:
                        if yellow.position.y < bullet.y < yellow.position.y + yellow.height:
                            # Collision detected with yellow spaceship
                            yellow.health -= bullet_damage
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
                                red.health -= bullet_damage
                                self.remove_bullet(bullet)

                                # Check if red spaceship's health reaches zero
                                if red.health <= 0:
                                    red.health = 0
                                    red.alive = False
                                    red.visible = False

            for enemy_ship in enemy_ships:
                if bullet.owner != "green":
                    if enemy_ship.position.x < bullet.x + bullet.radius < enemy_ship.position.x + enemy_ship.width:
                        if enemy_ship.position.y < bullet.y < enemy_ship.position.y + enemy_ship.height:
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
                                scoreboard.increase_score(100)
                

            for asteroid in asteroids:
                if bullet.owner != "green" and asteroid.alive and asteroid.visible:
                    if asteroid.position.x < bullet.x + bullet.radius < asteroid.position.x + asteroid.radius * 2:
                        if asteroid.position.y < bullet.y < asteroid.position.y + asteroid.radius * 2:
                            # Collision detected with asteroid
                            asteroid.health -= bullet_damage
                            asteroid.damage = asteroid.health
                            self.remove_bullet(bullet)

                            # Check if asteroid's health reaches zero
                            if asteroid.health <= 0:
                                asteroid.stop_moving()
                                asteroid.visible = False

                                asteroid.position.x = WIDTH
                                asteroid.position.y = HEIGHT
                                asteroid.health = 5
                                asteroid.visible = True
                                scoreboard.increase_score(100)

                #green bullet and asteroid collision
                #elif bullet.owner == "green" and asteroid.alive and asteroid.visible: 
                 #   if asteroid.position.x < bullet.x + bullet.radius < asteroid.position.x + asteroid.radius * 2:
                  #      if asteroid.position.y < bullet.y < asteroid.position.y + asteroid.radius * 2:
                   #         self.remove_bullet(bullet)



    def handle_ship_asteroid_collision(self, ship, asteroids, WIDTH, HEIGHT,scoreboard):
        for asteroid in asteroids:
            if ship.alive and ship.visible and asteroid.alive and asteroid.visible:
                if ship.position.x < asteroid.position.x + asteroid.radius * 2 and \
                ship.position.x + ship.width > asteroid.position.x and \
                ship.position.y < asteroid.position.y + asteroid.radius * 2 and \
                ship.position.y + ship.height > asteroid.position.y:
                    # Collision detected between ship and asteroid
                    ship.health -= asteroid.collision_damage
                    asteroid.health -= ship.collision_damage

                    # Check if ship's health reaches zero
                    if ship.health <= 0:
                        ship.health = 0
                        ship.alive = False
                        ship.visible = False
                    if asteroid.health <= 0:
                        asteroid.stop_moving()
                        asteroid.visible = False

                        asteroid.position.x = WIDTH
                        asteroid.position.y = HEIGHT
                        asteroid.health = self.health = random.randint(5, 15)
                        asteroid.visible = True
                        scoreboard.increase_score(100)
    
    def handle_enemyship_ship_collision(self, ship, enemy_ships, WIDTH, HEIGHT,scoreboard):
        for enemyship in enemy_ships:
            if ship.alive and ship.visible and enemyship.alive and enemyship.visible:
                if ship.position.x < enemyship.position.x + enemyship.width and \
                        ship.position.x + ship.width > enemyship.position.x and \
                        ship.position.y < enemyship.position.y + enemyship.height and \
                        ship.position.y + ship.height > enemyship.position.y:
                    # Collision detected between yellow player ship and enemy ship
                    ship.health -= enemyship.collision_damage  # Reduce yellow player ship's health based on enemy ship's damage
                    enemyship.health -= ship.collision_damage  # Reduce enemy ship's health based on yellow player ship's damage

                    if ship.health <= 0:
                        ship.alive = False
                        ship.visible = False
                        # Handle yellow player ship's destruction

                    if enemyship.health <= 0:
                        
                        enemyship.stop_moving()
                        enemyship.visible = False

                        enemyship.position.x = WIDTH
                        enemyship.position.y = HEIGHT
                        enemyship.health = 10
                        enemyship.visible = True
                        scoreboard.increase_score(100)




    def handle_enemy_asteroid_collision(self,enemy_ships,asteroids,WIDTH,HEIGHT):
        for enemy_ship in enemy_ships:
            if enemy_ship.alive and enemy_ship.visible:
                for asteroid in asteroids:
                    if enemy_ship.alive and enemy_ship.visible and asteroid.alive and asteroid.visible:
                        if enemy_ship.position.x < asteroid.position.x + asteroid.radius * 2 and \
                        enemy_ship.position.x + enemy_ship.width > asteroid.position.x and \
                        enemy_ship.position.y < asteroid.position.y + asteroid.radius * 2 and \
                        enemy_ship.position.y + enemy_ship.height > asteroid.position.y:

                            asteroid.stop_moving()
                            asteroid.visible = False

                            asteroid.position.x = WIDTH
                            asteroid.position.y = HEIGHT
                            asteroid.health =  self.health = random.randint(5, 15) 
                            asteroid.visible = True

            






            
