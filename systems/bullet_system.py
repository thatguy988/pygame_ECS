import pygame
import random
import time
from components.bullet import Bullet
from components.score import Score
from components.explosion import Explosion, load_explosion_images

from systems.sound_effect_system import SoundEffectSystem


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)    
RED = (255, 0, 0)
GREEN = (0,255,0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)
BROWN = (165, 42, 42)
WIDTH, HEIGHT = 1400, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

maximum_y_value = HEIGHT - 25
minimum_y_value = HEIGHT - maximum_y_value



green_ship_points = 10
asteroid_points = 5

sound_system_instance = SoundEffectSystem()
sound_system_instance.load_sound_effects()







class BulletSystem:
    def __init__(self):
        self.bullets = []
        

    
    def create_bullet(self, x, y, x_velocity, y_velocity, radius, owner,width_increase = 0, height_increase = 0):
        bullet = Bullet(x, y, x_velocity, y_velocity, radius, owner)
        bullet.increase_size(width_increase, height_increase)
        self.bullets.append(bullet)
    
    def fire_bullet(self, player, last_bullet_time, player_bullet_delay, stage,pause_duration,game_start_time, color):
        current_time = pygame.time.get_ticks() - pause_duration - game_start_time
        time_since_last_bullet = current_time - last_bullet_time

        if time_since_last_bullet >= player_bullet_delay:
            # x, y, xvelocity, yvelocity, radius, owner
            sound_system_instance.play_sound_effect("bulletshot")
            if stage <= 1:  # stage 0, 1
                self.create_bullet(
                    player.position.x + player.width,
                    player.position.y + player.height // 2,
                    5, 0, 10, color
                )
            if stage >= 2:  # stage 2, 3
                self.create_bullet(
                    player.position.x + player.width,
                    player.position.y + player.height // 2 - 5,
                    5, 0, 10, color
                )
                self.create_bullet(
                    player.position.x + player.width,
                    player.position.y + player.height // 2 + 10,
                    5, 0, 10, color
                )
            if stage >= 4:  # stage 4, 5
                self.create_bullet(
                    player.position.x + player.width,
                    player.position.y + player.height // 2 - 7,
                    5, -0.25, 10, color
                )
                self.create_bullet(
                    player.position.x + player.width,
                    player.position.y + player.height // 2 + 12,
                    5, 0.25, 10, color
                )
            if stage >= 6:  # stage 6, 7
                self.create_bullet(
                    player.position.x + player.width,
                    player.position.y + player.height // 2 - 7,
                    5, -0.5, 10, color
                )
                self.create_bullet(
                    player.position.x + player.width,
                    player.position.y + player.height // 2 + 12,
                    5, 0.5, 10, color
                )

            last_bullet_time = current_time

        return last_bullet_time


    def fire_bullets(self, yellow, red, player_count, last_bullet_time, last_bullet_time_2, pause_duration,game_start_time, stage):
        player_bullet_delay = 300

        if player_count >= 1 and yellow.alive:
            bullet_pressed = pygame.key.get_pressed()[pygame.K_SPACE]
            if bullet_pressed:
                last_bullet_time = self.fire_bullet(
                    yellow, last_bullet_time, player_bullet_delay, stage,pause_duration,game_start_time, "yellow"
                )

        if player_count == 2 and red.alive:
            bullet_pressed_2 = pygame.key.get_pressed()[pygame.K_RETURN]
            if bullet_pressed_2:
                last_bullet_time_2 = self.fire_bullet(
                    red, last_bullet_time_2, player_bullet_delay, stage,pause_duration,game_start_time, "red"
                )

        return last_bullet_time, last_bullet_time_2
    
    def remove_offscreen_bullets(self, width, height):
        '''
        removed_bullets = [
            bullet for bullet in self.bullets
            if bullet.x < 0 or bullet.x > width or bullet.y < 0 or bullet.y > height
        ]
        '''

        self.bullets = [
            bullet for bullet in self.bullets
            if 0 <= bullet.x <= width and 0 <= bullet.y <= height
        ]

        


    
    def remove_bullet(self, bullet):
        if bullet in self.bullets:
            self.bullets.remove(bullet)
    
    def render_bullets(self, surface):
        for bullet in self.bullets:
            if bullet.owner == "yellow":
                bullet_color = YELLOW  # Yellow color
            elif bullet.owner == "red":
                bullet_color = RED  # Red color
            elif bullet.owner == "green":
                bullet_color = GREEN #green color
            elif bullet.owner == "orange":
                bullet_color = ORANGE
            elif bullet.owner == "purple":
                bullet_color = PURPLE
            elif bullet.owner == "blue":
                bullet_color = BLUE
            elif bullet.owner == "brown":
                bullet_color = BROWN
            else:
                bullet_color = WHITE  # Default color (white)

            pygame.draw.rect(surface, bullet_color, (bullet.x, bullet.y, bullet.width, bullet.height))
    
    
        
    def auto_fire(self, enemy_ships, pause_duration, game_start_time, *last_bullet_times):
        current_time = pygame.time.get_ticks() - pause_duration - game_start_time
        time_since_last_bullets = [current_time - last_bullet_time for last_bullet_time in last_bullet_times]
        color_delays = {
            "green": 2000,  
            "orange": 1500,  
            "purple": 1200,
            "blue": 500,
            "brown": 1600,
            "white": 1800,
        }
        for enemy_ship in enemy_ships:
            if hasattr(enemy_ship, "ship_color") and enemy_ship.ship_color in color_delays:
                delay = color_delays[enemy_ship.ship_color]
                if enemy_ship.ship_color == "green" and time_since_last_bullets[0] >= delay:
                    self.create_bullet(
                        enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2 - 10, -5, 0, 10, "green"
                    )
                    self.create_bullet(
                        enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2 + 10, -5, 0, 10, "green"
                    )
                    sound_system_instance.play_sound_effect("enemyshot")
                    last_bullet_times = list(last_bullet_times)  # Convert tuple to list
                    last_bullet_times[0] = current_time  # Update the first item
                    last_bullet_times = tuple(last_bullet_times)  # Convert list back to tuple

                elif enemy_ship.ship_color == "orange" and time_since_last_bullets[1] >= delay:
                    

                    self.create_bullet(
                        enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2, -5, 0, 10, "orange"
                    )
                    sound_system_instance.play_sound_effect("enemyshot")

                    last_bullet_times = list(last_bullet_times)  # Convert tuple to list
                    last_bullet_times[1] = current_time  # Update the second item
                    last_bullet_times = tuple(last_bullet_times)  # Convert list back to tuple

                elif enemy_ship.ship_color == "purple" and time_since_last_bullets[2] >= delay:
                    if enemy_ship.bullet_switch:
                        self.create_bullet(
                            enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2, -5, -0.5, 10, "purple"
                        )
                    else:
                        self.create_bullet(
                            enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2, -5, 0.5, 10, "purple"
                        )
                    sound_system_instance.play_sound_effect("enemyshot")

                    last_bullet_times = list(last_bullet_times)  # Convert tuple to list
                    last_bullet_times[2] = current_time  # Update the third item
                    last_bullet_times = tuple(last_bullet_times)  # Convert list back to tuple
                    enemy_ship.bullet_switch = not enemy_ship.bullet_switch

                elif enemy_ship.ship_color == "blue" and time_since_last_bullets[3] >= delay:
                            self.create_bullet(
                                enemy_ship.position.x + 10 , enemy_ship.position.y + enemy_ship.height // 2, 0, 1, 10, "blue"
                            )
                            self.create_bullet(
                                enemy_ship.position.x + 10 , enemy_ship.position.y + enemy_ship.height // 2, 0, 1, 10, "blue"
                            )
                            sound_system_instance.play_sound_effect("enemyshot")

                            last_bullet_times = list(last_bullet_times)  # Convert tuple to list
                            last_bullet_times[3] = current_time  # Update the fourth item
                            last_bullet_times = tuple(last_bullet_times)  # Convert list back to tuple
                elif enemy_ship.ship_color == "brown" and time_since_last_bullets[4] >= delay:
                    self.create_bullet(
                            enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2 - 7, -5, -0.5, 10, "brown"
                        )
                    self.create_bullet(
                            enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2, -5, 0, 10, "brown"
                        )
                    self.create_bullet(
                            enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2 + 7, -5, 0.5, 10, "brown"
                        )
                    sound_system_instance.play_sound_effect("enemyshot")
                    last_bullet_times = list(last_bullet_times)  # Convert tuple to list
                    last_bullet_times[4] = current_time  # Update the fifth item
                    last_bullet_times = tuple(last_bullet_times)  # Convert list back to tuple

                elif enemy_ship.ship_color == "white" and time_since_last_bullets[5] >= delay:
                    if enemy_ship.bullet_change == 0:
                        bullet_params = [
                            (-5, -1.25),
                            (-5, -1),
                            (-5, -0.5),
                            (-5, 0),
                            (-5, 0.5),
                            (-5, 1),
                            (-5, 1.25)
                        ]

                        for x_offset, y_speed in bullet_params:
                            self.create_bullet(
                                enemy_ship.position.x - 5,
                                enemy_ship.position.y + enemy_ship.height // 2 + y_speed * 9,
                                x_offset,
                                y_speed,
                                100,
                                "white"
                            )
                        sound_system_instance.play_sound_effect("enemyshot")


                        enemy_ship.bullet_change = random.randint(0, 3)
                        last_bullet_times = list(last_bullet_times)
                        last_bullet_times[5] = current_time
                        last_bullet_times = tuple(last_bullet_times)
                    elif enemy_ship.bullet_change == 1:
                        if enemy_ship.bullet_beam == 0:
                            num_positions = random.randint(5, 8)
                            beam_height = 10
                            enemy_ship.beam_positions = generate_random_y_positions(num_positions, beam_height)
                        for beam_y_position in enemy_ship.beam_positions:
                            self.create_bullet(
                                enemy_ship.position.x - 5, beam_y_position - 5, -5, 0, 10, "white"
                            )
                            self.create_bullet(
                                enemy_ship.position.x - 5, beam_y_position, -5, 0, 10, "white"
                            )
                        enemy_ship.bullet_beam += 1
                        if enemy_ship.bullet_beam == 60:
                            enemy_ship.bullet_change = random.randint(0, 3)
                            enemy_ship.bullet_beam = 0
                            last_bullet_times = list(last_bullet_times)  # Convert tuple to list
                            last_bullet_times[5] = current_time  # Update the sixth item
                            last_bullet_times = tuple(last_bullet_times)  # Convert list back to tuple

                    elif(enemy_ship.bullet_change == 2):
                        self.create_bullet(
                                enemy_ship.position.x - 5, random.randint(5,495), -5, 0, 10, "white" 
                            )
                        enemy_ship.bullet_count +=1
                        if enemy_ship.bullet_count == enemy_ship.bullet_count_limit:
                            sound_system_instance.play_sound_effect("enemyshot")

                            enemy_ship.bullet_count = 0
                            enemy_ship.bullet_count_limit = random.randint(20,35)
                            enemy_ship.bullet_change = random.randint(0,3)
                            last_bullet_times = list(last_bullet_times)  # Convert tuple to list
                            last_bullet_times[5] = current_time  # Update the sixth item
                            last_bullet_times = tuple(last_bullet_times)  # Convert list back to tuple

                    elif(enemy_ship.bullet_change == 3):
                        bullet_width = 40
                        bullet_height = 40
                        num_of_bullets = random.randint(3,5)
                        y_positions = generate_random_y_positions(num_of_bullets,bullet_height)  
                        for y in y_positions:
                            self.create_bullet(
                                enemy_ship.position.x - 5, y, -5, 0, 100, "white", bullet_width, bullet_height
                            )
                       
                        enemy_ship.bullet_change = random.randint(0, 3)
                        last_bullet_times = list(last_bullet_times)  # Convert tuple to list
                        last_bullet_times[5] = current_time  # Update the sixth item
                        last_bullet_times = tuple(last_bullet_times)  # Convert list back to tuple

        return last_bullet_times
    
    def update_bullets_and_check_collisions(self, enemy_ships, WIDTH, yellow, red, player_count, background, HEIGHT, scoreboard, explosions):
        
        for bullet in self.bullets:
            bullet.update()

            if yellow.alive and yellow.visible and bullet.owner not in {"red", "yellow"}:
                if yellow.position.x < bullet.x + bullet.radius < yellow.position.x + yellow.width and yellow.position.y < bullet.y < yellow.position.y + yellow.height:
                    # Collision detected with yellow spaceship bullet from enemy ship
                    yellow.health = max(0, yellow.health - bullet.get_bullet_damage())
                    self.remove_bullet(bullet)
                    sound_system_instance.play_sound_effect("playerhit")

                    # Check if yellow spaceship's health reaches zero
                    if yellow.health == 0:
                        yellow.alive = False
                        yellow.visible = False
                        sound_system_instance.play_sound_effect("playerdeath")


            if player_count == 2 and red.alive and red.visible and bullet.owner not in {"yellow", "red"}:
                if red.position.x < bullet.x + bullet.radius < red.position.x + red.width and red.position.y < bullet.y < red.position.y + red.height:
                    # Collision detected with red spaceship
                    red.health = max(0, red.health - bullet.get_bullet_damage())
                    self.remove_bullet(bullet)
                    sound_system_instance.play_sound_effect("playerhit")

                    # Check if red spaceship's health reaches zero
                    if red.health == 0:
                        red.alive = False
                        red.visible = False
                        sound_system_instance.play_sound_effect("playerdeath")

            for enemy_ship in enemy_ships:
                if bullet.owner not in ["green", "orange", "purple", "blue", "brown", "white","grey"]:
                    if enemy_ship.position.x < bullet.x + bullet.radius < enemy_ship.position.x + enemy_ship.width:
                        if enemy_ship.position.y < bullet.y < enemy_ship.position.y + enemy_ship.height:
                            # Collision detected with enemy spaceship
                            enemy_ship.health -= bullet.get_bullet_damage()
                            health_reward = bullet.owner
                            self.remove_bullet(bullet)
                            sound_system_instance.play_sound_effect("enemyhit")

                            # Check if enemy spaceship's health reaches zero
                            if enemy_ship.health <= 0:
                                health(health_reward,yellow,red)
                                explosion = Explosion(enemy_ship.position.x, enemy_ship.position.y)

                                explosions.append(explosion)
                                enemy_ship.stop_moving()
                                enemy_ship.alive = False
                                #print("Before removal:", enemy_ships)
                                scoreboard.reward_points(enemy_ship.ship_color)






                                enemy_ships.remove(enemy_ship)
                                #print("After removal:", enemy_ships)
                                

                                #sound_system_instance.play_sound_effect("explosion")
            


       
    
    



    def handle_enemyship_ship_collision(self, ship, enemy_ships,scoreboard,explosions):
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
                        explosion = Explosion(enemy_ship.position.x, enemy_ship.position.y)

                        explosions.append(explosion)
                        enemy_ship.stop_moving()
                        enemy_ship.alive = False
                        #print("Before removal:", enemy_ships)
                        scoreboard.reward_points(enemy_ship.ship_color)

                        enemy_ships.remove(enemy_ship)
                       # print("After removal:", enemy_ships)



def health(health_reward,yellow,red):
        if health_reward == "yellow":
            yellow.health += 5
        elif health_reward == "red":
            red.health += 5

def generate_random_y_positions(num_positions, bullet_height):
    positions = []
    while len(positions) < num_positions:
        y = random.randint(5, 495)
        if all(abs(y - existing_y) > bullet_height for existing_y in positions) and all(abs(y - existing_y) != bullet_height for existing_y in positions):
            positions.append(y)
    return positions