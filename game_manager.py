import pygame
import config
from pygame import freetype



from components.ship import ShipCreation
from components.score import Score



from systems.explosion_system import ExplosionSystem
from systems.bullet_system import BulletSystem
from systems.movement import MovementSystem
from systems.render import RenderSystem







class GameManager:
    def __init__(self):
        self.yellow = None
        self.red = None

        self.score_limit = None
        self.scoreboard = None

        self.enemy_ships = []
        self.background = None
        self.pre_rendered_background = None
        self.text_backbuffer = pygame.Surface((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))


        
        self.last_bullet_time = 0
        self.last_bullet_time_2 = 0

        self.boss = None

        self.last_asteroid_spawn_time = 0
        self.last_spawn_time_green_ships = 0
        self.last_spawn_time_orange_ships = 0
        self.last_spawn_time_purple_ships = 0
        self.last_spawn_time_blue_ships = 0
        self.last_spawn_time_brown_ships = 0

        self.last_bullet_time_green_ship = 0
        self.last_bullet_time_orange_ship = 0
        self.last_bullet_time_purple_ship = 0
        self.last_bullet_time_blue_ship = 0
        self.last_bullet_time_brown_ship = 0
        self.last_bullet_time_white_ship = 0

        self.pause_pressed = False
        self.game_paused = False

        self.font = None
        self.text_display_duration = 5000
        self.prev_score = None
        self.score_text = None
        self.score_rect = None

        self.prev_yellow_health = None
        self.prev_red_health = None
        self.yellow_health_text = None
        self.red_health_text = None

        self.run = True
        self.clock = None

        self.fps= None
        self.fps_text = None
        self.fps_rect = None


        self.pause_duration = 0
        self.game_start_time = None
        self.current_time = None
        self.last_score_change = None
        self.last_yellow_health_change = None
        self.last_red_health_change = None

        self.explosion_system_instance = ExplosionSystem()
        self.bullet_system_instance = BulletSystem(self.explosion_system_instance)
        self.movement_system_instance = MovementSystem()
        self.render_system_instance = RenderSystem()

    def reset_game(self,player_count,stage):
        # Reset instances
        self.explosion_system_instance.reset()
        self.bullet_system_instance.reset()
        


        # Reset game-specific variables
        self.yellow = ShipCreation.create_yellow_ship()
        self.red = ShipCreation.create_red_ship() if player_count == 2 else None

        self.score_limit = Score.set_score_limit(stage)
        self.scoreboard = Score(self.score_limit)

        self.enemy_ships = []

        self.background = self.render_system_instance.background_render(stage, config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)
        self.pre_rendered_background = pygame.Surface((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
        scaled_background = pygame.transform.scale(self.background, (config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
        self.pre_rendered_background.blit(scaled_background, (0, 0))

        self.last_bullet_time = 0
        self.last_bullet_time_2 = 0

        self.boss = ShipCreation.create_boss_enemy_ship() if stage == 7 else None
        if self.boss is not None:
            self.enemy_ships.append(self.boss)

        self.last_asteroid_spawn_time = 0
        self.last_spawn_time_green_ships = 0
        self.last_spawn_time_orange_ships = 0
        self.last_spawn_time_purple_ships = 0
        self.last_spawn_time_blue_ships = 0
        self.last_spawn_time_brown_ships = 0

        self.last_bullet_time_green_ship = 0
        self.last_bullet_time_orange_ship = 0
        self.last_bullet_time_purple_ship = 0
        self.last_bullet_time_blue_ship = 0
        self.last_bullet_time_brown_ship = 0
        self.last_bullet_time_white_ship = 0

        self.pause_pressed = False
        self.game_paused = False
       
        
        self.font = pygame.font.Font(None, 24)
        self.text_display_duration = 5000
        
        self.prev_score = self.scoreboard.score
        self.score_text = self.font.render("Score: " + str(self.scoreboard.score), True, (255, 255, 255))
        self.score_rect = self.score_text.get_rect(midtop=(config.DISPLAY_WIDTH // 2, 10))

        self.prev_yellow_health = self.yellow.health
        self.prev_red_health = self.red.health if player_count == 2 else None
        self.yellow_health_text = self.font.render("Yellow Health: " + str(self.yellow.health), True, (255, 255, 255))
        self.red_health_text = self.font.render("Red Health: " + str(self.red.health), True, (255, 255, 255)) if player_count == 2 else None

        self.run = True
        self.clock = pygame.time.Clock()

        self.fps = self.clock.get_fps()
        self.fps_text = self.font.render("FPS: " + str(int(self.fps)), True, (255, 255, 255))
        self.fps_rect = self.fps_text.get_rect(topright=(config.DISPLAY_WIDTH - 10, 10))
        

                
        

        


        
        

        self.pause_start_time = pygame.time.get_ticks()
        self.pause_end_time = pygame.time.get_ticks()
        self.pause_duration += self.pause_end_time - self.pause_start_time

        self.game_start_time = pygame.time.get_ticks()
        self.current_time = pygame.time.get_ticks() - self.pause_duration - self.game_start_time
        self.last_score_change = pygame.time.get_ticks() - self.pause_duration - self.game_start_time
        self.last_yellow_health_change = pygame.time.get_ticks() - self.pause_duration - self.game_start_time
        self.last_red_health_change = pygame.time.get_ticks() - self.pause_duration - self.game_start_time if player_count == 2 else None
    #@profile
    def update_game_state(self, yellow, red, enemy_ships, player_count, keys_pressed, pre_rendered_background, scoreboard):
        if player_count >= 1:
            self.movement_system_instance.move_player1(
                yellow, keys_pressed, config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT, yellow.velocity, yellow.width, yellow.height
            )

        if player_count == 2:
            self.movement_system_instance.move_player2(
                red, keys_pressed, config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT, red.velocity, red.width, red.height
            )
        self.movement_system_instance.move_enemy_ships(enemy_ships, config.DISPLAY_WIDTH)  # Move all enemy ships


        if player_count == 2:
            self.render_system_instance.draw_window([yellow, red] + enemy_ships, self.bullet_system_instance, pre_rendered_background)
        else:
            self.render_system_instance.draw_window([yellow] + enemy_ships, self.bullet_system_instance, pre_rendered_background)

        if player_count == 2:
            self.bullet_system_instance.handle_enemyship_ship_collision(red, enemy_ships, scoreboard)

        self.bullet_system_instance.handle_enemyship_ship_collision(yellow, enemy_ships, scoreboard)
        self.bullet_system_instance.update_bullets_and_check_collisions(enemy_ships, yellow, red, player_count, scoreboard)
        self.bullet_system_instance.remove_offscreen_bullets(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)
        if self.explosion_system_instance.explosions:
            self.explosion_system_instance.update_explosions()
            self.render_system_instance.render_explosion(self.explosion_system_instance, config.WIN)


