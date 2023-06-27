import pygame
import random
import config
from components.bullet import Bullet

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


maximum_y_value = config.DISPLAY_HEIGHT - 25
minimum_y_value = config.DISPLAY_HEIGHT - maximum_y_value

sound_system_instance = SoundEffectSystem()
sound_system_instance.load_sound_effects()


class BulletSystem:
    def __init__(self,explosion_system_instance):
        self.bullets = []
        self.explosion_system = explosion_system_instance

    def reset(self):
        self.bullets = []

    def create_bullet(self, x, y, x_velocity, y_velocity, owner,width_increase = 0, height_increase = 0):
        bullet = Bullet(x, y, x_velocity, y_velocity, owner)
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
                    5, 0, color
                )
            if stage >= 2:  # stage 2, 3
                self.create_bullet(
                    player.position.x + player.width,
                    player.position.y + player.height // 2 - 5,
                    5, 0, color
                )
                self.create_bullet(
                    player.position.x + player.width,
                    player.position.y + player.height // 2 + 10,
                    5, 0, color
                )
            if stage >= 4:  # stage 4, 5
                self.create_bullet(
                    player.position.x + player.width,
                    player.position.y + player.height // 2 - 7,
                    5, -0.25, color
                )
                self.create_bullet(
                    player.position.x + player.width,
                    player.position.y + player.height // 2 + 12,
                    5, 0.25, color
                )
            if stage >= 6:  # stage 6, 7
                self.create_bullet(
                    player.position.x + player.width,
                    player.position.y + player.height // 2 - 7,
                    5, -0.5, color
                )
                self.create_bullet(
                    player.position.x + player.width,
                    player.position.y + player.height // 2 + 12,
                    5, 0.5, color
                )

            last_bullet_time = current_time

        return last_bullet_time


    def fire_bullets(self, yellow, red, player_count, last_bullet_time, last_bullet_time_2, pause_duration,game_start_time, stage, dt):
        player_bullet_delay = 300 * dt

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
    
    def remove_offscreen_bullets(self):
        self.bullets = [
            bullet for bullet in self.bullets
            if 0 <= bullet.x <= config.DISPLAY_WIDTH and 0 <= bullet.y <= config.DISPLAY_HEIGHT
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
    
    
        
    def auto_fire(self, enemy_ships, pause_duration, game_start_time, dt, *last_bullet_times):
        current_time = pygame.time.get_ticks() - pause_duration - game_start_time
        #delta_time = current_time - previous_time
        #previous_time = current_time
        time_since_last_bullets = [current_time - last_bullet_time for last_bullet_time in last_bullet_times]
        color_delays = {
            "green": 2500,  
            "orange": 1800,  
            "purple": 1000,
            "blue": 500,
            "brown": 1400,
            "white": 1200,
        }
        for enemy_ship in enemy_ships:
            if hasattr(enemy_ship, "ship_color") and enemy_ship.ship_color in color_delays:
                delay = color_delays[enemy_ship.ship_color] * dt
                if enemy_ship.ship_color == "green" and time_since_last_bullets[0] >= delay:
                    self.create_bullet(
                        enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2 - 10, -5, 0, "green"
                    )
                    self.create_bullet(
                        enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2 + 10, -5, 0, "green"
                    )
                    sound_system_instance.play_sound_effect("enemyshot")
                    last_bullet_times = list(last_bullet_times)  # Convert tuple to list
                    last_bullet_times[0] = current_time  # Update the first item
                    last_bullet_times = tuple(last_bullet_times)  # Convert list back to tuple

                elif enemy_ship.ship_color == "orange" and time_since_last_bullets[1] >= delay:
                    

                    self.create_bullet(
                        enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2, -5, 0, "orange"
                    )
                    sound_system_instance.play_sound_effect("enemyshot")

                    last_bullet_times = list(last_bullet_times)  # Convert tuple to list
                    last_bullet_times[1] = current_time  # Update the second item
                    last_bullet_times = tuple(last_bullet_times)  # Convert list back to tuple

                elif enemy_ship.ship_color == "purple" and time_since_last_bullets[2] >= delay:
                    if enemy_ship.bullet_switch:
                        self.create_bullet(
                            enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2, -5, -0.5, "purple"
                        )
                    else:
                        self.create_bullet(
                            enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2, -5, 0.5, "purple"
                        )
                    sound_system_instance.play_sound_effect("enemyshot")

                    last_bullet_times = list(last_bullet_times)  # Convert tuple to list
                    last_bullet_times[2] = current_time  # Update the third item
                    last_bullet_times = tuple(last_bullet_times)  # Convert list back to tuple
                    enemy_ship.bullet_switch = not enemy_ship.bullet_switch

                elif enemy_ship.ship_color == "blue" and time_since_last_bullets[3] >= delay:
                            self.create_bullet(
                                enemy_ship.position.x + 10 , enemy_ship.position.y + enemy_ship.height // 2, 0, 1, "blue"
                            )
                            self.create_bullet(
                                enemy_ship.position.x + 10 , enemy_ship.position.y + enemy_ship.height // 2, 0, 1, "blue"
                            )
                            sound_system_instance.play_sound_effect("enemyshot")

                            last_bullet_times = list(last_bullet_times)  # Convert tuple to list
                            last_bullet_times[3] = current_time  # Update the fourth item
                            last_bullet_times = tuple(last_bullet_times)  # Convert list back to tuple
                elif enemy_ship.ship_color == "brown" and time_since_last_bullets[4] >= delay:
                    self.create_bullet(
                            enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2 - 7, -5, -0.5, "brown"
                        )
                    self.create_bullet(
                            enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2, -5, 0, "brown"
                        )
                    self.create_bullet(
                            enemy_ship.position.x - 5, enemy_ship.position.y + enemy_ship.height // 2 + 7, -5, 0.5, "brown"
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
                                "white",0,0
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
                                enemy_ship.position.x - 5, beam_y_position - 5, -5, 0, "white",0,0
                            )
                            self.create_bullet(
                                enemy_ship.position.x - 5, beam_y_position, -5, 0, "white",0,0
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
                                enemy_ship.position.x - 5, random.randint(5,495), -5, 0, "white",0,0 
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
                                enemy_ship.position.x - 5, y, -5, 0, "white", bullet_width, bullet_height
                            )
                       
                        enemy_ship.bullet_change = random.randint(0, 3)
                        last_bullet_times = list(last_bullet_times)  # Convert tuple to list
                        last_bullet_times[5] = current_time  # Update the sixth item
                        last_bullet_times = tuple(last_bullet_times)  # Convert list back to tuple

        return last_bullet_times
    

    def check_bullet_collision(self, bullet, entity):
        bullet_offset = 15 # Adjust this value as needed

        bullet_rect = pygame.Rect(bullet.x - bullet.width/2, bullet.y - bullet.height/2, bullet.width, bullet.height)
        entity_rect = pygame.Rect(entity.position.x - bullet_offset, entity.position.y, entity.width - bullet_offset, entity.height)
        return bullet_rect.colliderect(entity_rect)
    

    def check_ship_collision(self, entity1, entity2):
        entity1_rect = pygame.Rect(entity1.position.x, entity1.position.y, entity1.width, entity1.height)
        entity2_rect = pygame.Rect(entity2.position.x, entity2.position.y, entity2.width, entity2.height)
        return entity1_rect.colliderect(entity2_rect)

    

    #bounding box algorithm
    
    def update_bullets_and_check_collisions(self, enemy_ships, yellow, red, player_count, scoreboard , dt):
        for bullet in self.bullets:
            bullet.update(dt)

            if yellow.alive and yellow.visible and bullet.owner not in {"red", "yellow"}:
                if self.check_bullet_collision(bullet, yellow):
                    yellow.health = max(0, yellow.health - bullet.get_bullet_damage())
                    self.remove_bullet(bullet)
                    sound_system_instance.play_sound_effect("playerhit")

                    if yellow.health <= 0 and yellow.alive:
                        yellow.alive = False
                        yellow.visible = False
                        sound_system_instance.play_sound_effect("playerdeath")

            if player_count == 2 and red.alive and red.visible and bullet.owner not in {"yellow", "red"}:
                if self.check_bullet_collision(bullet, red):
                    red.health = max(0, red.health - bullet.get_bullet_damage())
                    self.remove_bullet(bullet)
                    sound_system_instance.play_sound_effect("playerhit")

                    if red.health <= 0 and red.alive:
                        red.alive = False
                        red.visible = False
                        sound_system_instance.play_sound_effect("playerdeath")

            for enemy_ship in enemy_ships:
                if bullet.owner not in ["green", "orange", "purple", "blue", "brown", "white", "grey"]:
                    if self.check_bullet_collision(bullet, enemy_ship):
                        enemy_ship.health -= bullet.get_bullet_damage()
                        health_reward = bullet.owner
                        self.remove_bullet(bullet)
                        sound_system_instance.play_sound_effect("enemyhit")

                        if enemy_ship.health <= 0:
                            health(health_reward, yellow, red)
                            self.explosion_system.create_explosion(enemy_ship.position.x, enemy_ship.position.y)
                            enemy_ship.stop_moving()
                            scoreboard.reward_points(enemy_ship.ship_color)
                            enemy_ships.remove(enemy_ship)
    
    def handle_enemyship_ship_collision(self, ship, enemy_ships, scoreboard):
        for enemy_ship in enemy_ships:
            if ship.alive and ship.visible and enemy_ship.alive and enemy_ship.visible:
                if self.check_ship_collision(ship, enemy_ship):
                    ship.health -= enemy_ship.collision_damage
                    enemy_ship.health -= ship.collision_damage

                    if ship.health <= 0:
                        ship.alive = False
                        ship.visible = False

                    if enemy_ship.health <= 0:
                        # self.explosion_system.create_explosion(enemy_ship.position.x, enemy_ship.position.y)
                        enemy_ship.stop_moving()
                        enemy_ship.alive = False
                        scoreboard.reward_points(enemy_ship.ship_color)
                        enemy_ships.remove(enemy_ship)

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