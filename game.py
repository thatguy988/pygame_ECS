import pygame
import sys
import time

from game_manager import GameManager

from systems.render import RenderSystem
from systems.ship_system import create_ships
from systems.menu_input_system import MenuHandling
from systems.music_system import MusicSystem
from systems.sound_effect_system import SoundEffectSystem

from components.explosion import Explosion 

WIDTH, HEIGHT = 1400, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)    
RED = (255, 0, 0)


FPS = 120
VEL = 4

game_manager=GameManager()

music_system_instance = MusicSystem()

music_system_instance.add_music_component("pause_menu_music", "Assets\\Music\\mixkit-space-game-668.mp3")
music_system_instance.add_music_component("main_menu_music", "Assets\\Music\\mixkit-infected-vibes-157.mp3")



sound_system_instance = SoundEffectSystem()
sound_system_instance.load_sound_effects()

Explosion.load_explosion_images()



def select_players_screen():
    selected_option = 0
    while True:
        RenderSystem.display_select_players_screen(selected_option)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        sound_system_instance.play_sound_effect("menu_scrolling")

                        selected_option = (selected_option - 1) % 3  # Move up in the options list
                    elif event.key == pygame.K_s:
                        sound_system_instance.play_sound_effect("menu_scrolling")

                        selected_option = (selected_option + 1) % 3  # Move down in the options list
                    elif event.key == pygame.K_SPACE:
                        sound_system_instance.play_sound_effect("press_button")

                        if selected_option == 0:
                            return 1  # 1 player selected
                        elif selected_option == 1:
                            return 2  # 2 players selected
                        elif selected_option == 2:
                            return 0  # Back to main menu
        
        
def select_stage_screen():
    selected_option = 0
    while True:
        RenderSystem.display_select_stage_screen(selected_option)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    sound_system_instance.play_sound_effect("menu_scrolling")
                    selected_option = (selected_option - 1) % 8  # 7 for 7 options
                elif event.key == pygame.K_s:
                    sound_system_instance.play_sound_effect("menu_scrolling")
                    selected_option = (selected_option + 1) % 8  
                elif event.key == pygame.K_SPACE:
                    sound_system_instance.play_sound_effect("press_button")
                    if selected_option == 0:
                        return 1  # stage 1
                    elif selected_option == 1:
                        return 2  # stage 2
                    elif selected_option == 2:
                        return 3 # stage 3 
                    if selected_option == 3:
                        return 4 # stage 4
                    elif selected_option == 4:
                        return 5 # stage 5
                    elif selected_option == 5:
                        return 6  # stage 6
                    elif selected_option == 6:
                        return 7 #boss level
                    elif selected_option == 7:
                        return 0 # back


def main_menu(game_manager):
    music_system_instance.play_music("main_menu_music")
    music_system_instance.set_music_volume("main_menu_music", 0.3)

    selected_option = 0  # Default selected option
    while True:
        RenderSystem.display_menu(selected_option)
        selected_option = MenuHandling.handle_menu_events(selected_option)
        if selected_option == "start_game":
            player_count = select_players_screen()
            if player_count == 1:
                stage = select_stage_screen()  # Select the stage
                if(stage == 0):
                    continue #jump to next iteration of loop skip remaing code skips game_screen and selected option reset
                music_system_instance.stop_music("main_menu_music")
                story_screen(player_count,stage,game_manager)
            elif player_count == 2:
                stage = select_stage_screen()  # Select the stage
                if(stage == 0):
                    continue
                music_system_instance.stop_music("main_menu_music")
                story_screen(player_count,stage,game_manager)
            selected_option = 0  # Reset the selected option for when player goes back to main menu
        elif selected_option == "tutorial":
            player_count = select_players_screen()
            music_system_instance.stop_music("main_menu_music")
            game_screen(player_count,0,game_manager)
            selected_option = 0

def pause_menu(game_music):
    music_system_instance.pause_music(game_music)
    selected_option = 0  # Default selected option
    while True:
        RenderSystem.display_pause_menu(selected_option)
        selected_option = MenuHandling.handle_pause_menu_events(selected_option)
        if selected_option == "resume_game":
            music_system_instance.resume_music(game_music)
            return  # Resume the game
        elif selected_option == "main_menu":
            return "main_menu"  # Go back to the main menu

def game_over_screen(game_music,game_manager):
    music_system_instance.stop_music(game_music)
    sound_system_instance.play_sound_effect("game_over")
    while True:
        RenderSystem.display_game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    sound_system_instance.stop_sound_effect("game_over")
                    sound_system_instance.play_sound_effect("press_button")
                    return main_menu(game_manager)
                    


def next_stage_screen(player_count,stage,game_music,game_manager):
    music_system_instance.stop_music(game_music)
    while True:
        RenderSystem.display_next_stage_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    sound_system_instance.play_sound_effect("press_button")
                    result = story_screen(player_count,stage,game_manager)
                    if result == "main_menu":
                       main_menu(game_manager)
                       return

def story_screen(player_count,stage,game_manager):
    story_music=music_system_instance.load_story_music(stage)
    music_system_instance.play_music(story_music)
    music_system_instance.set_music_volume(story_music, 0.4)
    
    while True:
        RenderSystem.display_story_screen(stage)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    music_system_instance.stop_music(story_music)
                    sound_system_instance.play_sound_effect("press_button")

                    if(stage != 8):
                        result = game_screen(player_count,stage,game_manager)
                    else:
                        result = main_menu(game_manager)
                    if result == "main_menu":
                        main_menu(game_manager)
                        return
             

def game_screen(player_count,stage,game_manager):

    game_manager.reset_game(player_count,stage)
    game_music=music_system_instance.load_stage_music(stage)
    music_system_instance.play_music(game_music)
    music_system_instance.set_music_volume(game_music, 0.3)

    while game_manager.run:
        game_manager.clock.tick(FPS)
        
        if game_manager.scoreboard.has_score_limit_reached():
            next_stage_screen(player_count,stage + 1,game_music,game_manager)
            game_manager.run =False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_manager.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_manager.pause_pressed and not game_manager.game_paused:#in game screen is running we are pressing spacebar to shoot
                        pass
                    else: #press spacebar to resume game
                        game_manager.game_paused = False
                        result = pause_menu(game_music)
                        if result == "main_menu":
                            #never reached
                            return "main_menu"
                elif event.key == pygame.K_p:
                    if not game_manager.pause_pressed and not game_manager.game_paused:#game pause
                        game_manager.pause_pressed = True
                        game_manager.game_paused = True
                        game_manager.pause_start_time=pygame.time.get_ticks()
                        result = pause_menu(game_music)
                        if result == "resume_game":
                            game_manager.pause_pressed = False
                            game_manager.game_paused = False
                            result = None   
                        elif result == "main_menu":
                            music_system_instance.stop_music(game_music)
                            music_system_instance.play_music("main_menu_music")
                            return "main_menu"

        if game_manager.game_paused:
            game_manager.game_paused = False
            game_manager.pause_pressed = False
            result = None
            game_manager.pause_end_time=pygame.time.get_ticks()
            game_manager.pause_duration += game_manager.pause_end_time - game_manager.pause_start_time
            

        keys_pressed = pygame.key.get_pressed()
        game_manager.current_time = pygame.time.get_ticks() - game_manager.pause_duration - game_manager.game_start_time

        results = create_ships(game_manager.enemy_ships, game_manager.pause_duration, game_manager.game_start_time, stage, 
                               game_manager.last_spawn_time_green_ships, game_manager.last_asteroid_spawn_time, 
                               game_manager.last_spawn_time_orange_ships,game_manager.last_spawn_time_purple_ships, 
                               game_manager.last_spawn_time_blue_ships, game_manager.last_spawn_time_brown_ships)
        
        (
                game_manager.last_bullet_time_green_ship,
                game_manager.last_bullet_time_orange_ship,
                game_manager.last_bullet_time_purple_ship,
                game_manager.last_bullet_time_blue_ship,
                game_manager.last_bullet_time_brown_ship,
                game_manager.last_bullet_time_white_ship,
            ) = game_manager.bullet_system_instance.auto_fire(
                game_manager.enemy_ships,
                game_manager.pause_duration,
                game_manager.game_start_time,
                game_manager.last_bullet_time_green_ship,
                game_manager.last_bullet_time_orange_ship,
                game_manager.last_bullet_time_purple_ship,
                game_manager.last_bullet_time_blue_ship,
                game_manager.last_bullet_time_brown_ship,
                game_manager.last_bullet_time_white_ship,
            )

        if stage == 1:
            game_manager.last_spawn_time_green_ships = results[0]
            game_manager.last_asteroid_spawn_time = results[1]
        elif stage == 2:
            game_manager.last_spawn_time_green_ships = results[0]
            game_manager.last_spawn_time_orange_ships = results[1]
        elif stage == 3:
            game_manager.last_spawn_time_green_ships = results[0]
            game_manager.last_spawn_time_orange_ships = results[1]
            game_manager.last_spawn_time_purple_ships = results[2]
        elif stage == 4:
            game_manager.last_spawn_time_orange_ships = results[0]
            game_manager.last_spawn_time_purple_ships = results[1]
            game_manager.last_spawn_time_blue_ships = results[2]
        elif stage == 5:
            game_manager.last_spawn_time_orange_ships = results[0]
            game_manager.last_spawn_time_purple_ships = results[1]
            game_manager.last_spawn_time_blue_ships = results[2]
            game_manager.last_spawn_time_brown_ships = results[3]
        elif stage == 6:
            game_manager.last_spawn_time_purple_ships = results[0]
            game_manager.last_spawn_time_blue_ships = results[1]
            game_manager.last_spawn_time_brown_ships = results[2]
        elif stage == 0:
            game_manager.last_asteroid_spawn_time = results[0]
        
        
        game_manager.last_bullet_time, game_manager.last_bullet_time_2 = \
            game_manager.bullet_system_instance.fire_bullets(game_manager.yellow, game_manager.red, player_count, 
                                                             game_manager.last_bullet_time, game_manager.last_bullet_time_2,
                                                             game_manager.pause_duration,game_manager.game_start_time,stage)
        
        game_manager.update_game_state(game_manager.yellow, game_manager.red, game_manager.enemy_ships, player_count, keys_pressed, 
                                       game_manager.background,game_manager.scoreboard)
        
        if not game_manager.yellow.alive and player_count == 1:
            game_over_screen(game_music,game_manager)

        if player_count == 2:
            if not game_manager.red.alive and not game_manager.yellow.alive:
                game_over_screen(game_music,game_manager)
        
       
        if(player_count==1):
            game_manager.yellow_health_text, game_manager.last_yellow_health_change, game_manager.prev_yellow_health = \
                game_manager.render_system_instance.update_health_text(game_manager.current_time, game_manager.yellow, game_manager.red, 
                            game_manager.prev_yellow_health, game_manager.prev_red_health, game_manager.font, game_manager.last_yellow_health_change,
                            game_manager.last_red_health_change,game_manager.yellow_health_text,game_manager.red_health_text,player_count)
            
            game_manager.score_text, game_manager.last_score_change, game_manager.prev_score = \
                game_manager.render_system_instance.render_score(game_manager.scoreboard, game_manager.font,game_manager.prev_score,
                                          game_manager.last_score_change,game_manager.current_time,game_manager.score_text) 

        else:
            game_manager.yellow_health_text, game_manager.last_yellow_health_change, game_manager.prev_yellow_health, game_manager.red_health_text, game_manager.last_red_health_change, game_manager.prev_red_health = \
                game_manager.render_system_instance.update_health_text(game_manager.current_time, game_manager.yellow, game_manager.red, 
                            game_manager.prev_yellow_health, game_manager.prev_red_health, game_manager.font,game_manager.last_yellow_health_change,
                            game_manager.last_red_health_change,game_manager.yellow_health_text, game_manager.red_health_text, player_count)
            
            game_manager.score_text, game_manager.last_score_change, game_manager.prev_score = \
                game_manager.render_system_instance.render_score(game_manager.scoreboard, game_manager.font,game_manager.prev_score,
                                                                 game_manager.last_score_change,game_manager.current_time,game_manager.score_text) 

        if game_manager.current_time - game_manager.last_score_change < game_manager.text_display_duration:
            WIN.blit(game_manager.score_text, game_manager.score_rect)

        if game_manager.current_time - game_manager.last_yellow_health_change < game_manager.text_display_duration:
            WIN.blit(game_manager.yellow_health_text, (10, 10))

        if player_count == 2 and game_manager.current_time - game_manager.last_red_health_change < game_manager.text_display_duration:  
            WIN.blit(game_manager.red_health_text, (10, 30))
        if stage == 0:
            game_manager.render_system_instance.display_tutorial_instructions(player_count)
        

        game_manager.fps = game_manager.clock.get_fps()
        game_manager.fps_text = game_manager.font.render("FPS: " + str(int(game_manager.fps)), True, (255, 255, 255))
        game_manager.fps_rect = game_manager.fps_text.get_rect(topright=(WIDTH - 10, 10))
        WIN.blit(game_manager.fps_text, game_manager.fps_rect)
        
        
        pygame.display.update()
       
        game_manager.clock.tick(FPS)


def display_developer_screen(game_manager):
    #sound_system_instance.play_sound_effect("start_up_1")
    #sound_system_instance.play_sound_effect("start_up_2")
    display_duration = 8  # Duration in seconds
    start_time = time.time()

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time >= display_duration:
            
            main_menu(game_manager)
            return
        RenderSystem.display_developer_screen()

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    main_menu(game_manager)
                    return


def main():
    pygame.init()
    game_manager = GameManager()
    display_developer_screen(game_manager)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()