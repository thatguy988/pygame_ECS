import pygame
import sys


from systems.movement import MovementSystem
from systems.render import RenderSystem
from systems.bullet_system import BulletSystem
from systems.ship_system import create_ships
from systems.menu_input_system import MenuHandling
from systems.music_system import MusicSystem

from components.explosion import Explosion, load_explosion_images
from components.score import Score
from components.ship import ShipCreation

WIDTH, HEIGHT = 1400, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)    
RED = (255, 0, 0)


FPS = 120
VEL = 4


music_system_instance = MusicSystem()

music_system_instance.add_music_component("pause_menu_music", "Assets\\Music\\mixkit-space-game-668.mp3")
music_system_instance.add_music_component("main_menu_music", "Assets\\Music\\mixkit-infected-vibes-157.mp3")

def load_stage_music(stage):
    music_mapping = {
        1: "game_music_1",
        2: "game_music_2",
        3: "game_music_3",
        4: "game_music_4",
        5: "game_music_5",
        6: "game_music_6",
        7: "game_music_7",
        0: "game_music_0"
    }

    if stage in music_mapping:
        music_label = music_mapping[stage]
        music_system_instance.add_music_component(music_label, f"Assets\\Music\\game-music-{stage}.wav")
        return music_label

def load_story_music(stage):
    music_mapping = {
        1: "story_music_1",
        2: "story_music_2",
        3: "story_music_3",
        4: "story_music_4",
        5: "story_music_5",
        6: "story_music_6",
        7: "story_music_7",
        8: "story_music_8"
    }

    if stage in music_mapping:
        music_label = music_mapping[stage]
        music_system_instance.add_music_component(music_label, f"Assets\\Music\\story_music_{stage}.wav")
        return music_label
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
                        selected_option = (selected_option - 1) % 3  # Move up in the options list
                    elif event.key == pygame.K_s:
                        selected_option = (selected_option + 1) % 3  # Move down in the options list
                    elif event.key == pygame.K_SPACE:
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
                    selected_option = (selected_option - 1) % 8  # 7 for 7 options
                elif event.key == pygame.K_s:
                    selected_option = (selected_option + 1) % 8  
                elif event.key == pygame.K_SPACE:
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


def main_menu():
    music_system_instance.play_music("main_menu_music")
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
                story_screen(player_count,stage)
            elif player_count == 2:
                stage = select_stage_screen()  # Select the stage
                if(stage == 0):
                    continue
                music_system_instance.stop_music("main_menu_music")
                story_screen(player_count,stage)

            selected_option = 0  # Reset the selected option for when player goes back to main menu
        elif selected_option == "tutorial":
            player_count = select_players_screen()
            music_system_instance.stop_music("main_menu_music")
            game_screen(player_count,0)
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

def update_game_state(yellow, red, enemy_ships, player_count, keys_pressed, 
                      movement_system_instance, bullet_system_instance, render_system_instance, background,scoreboard,explosions):
    if player_count >= 1:
        movement_system_instance.move_player1(
            yellow, keys_pressed, WIDTH, HEIGHT, VEL, yellow.width, yellow.height
        )

    if player_count == 2:
        movement_system_instance.move_player2(
            red, keys_pressed, WIDTH, HEIGHT, VEL, yellow.width, yellow.height
        )

    if player_count == 2:
        render_system_instance.draw_window([yellow, red] + enemy_ships, bullet_system_instance, background)
    else:
        render_system_instance.draw_window([yellow] + enemy_ships,bullet_system_instance, background)
    if player_count == 2:
        bullet_system_instance.handle_enemyship_ship_collision(red, enemy_ships, WIDTH, HEIGHT,scoreboard)
    else:
        bullet_system_instance.handle_enemyship_ship_collision(yellow, enemy_ships, WIDTH, HEIGHT,scoreboard)

    bullet_system_instance.update_bullets_and_check_collisions(enemy_ships, WIDTH, yellow, red, player_count,background,HEIGHT,scoreboard,explosions)

    if not yellow.alive and player_count == 1:
            game_over_screen()

    if player_count == 2:
        if not red.alive and not yellow.alive:
                game_over_screen()

def game_over_screen():
    while True:
        RenderSystem.display_game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_menu()
                    return 


def next_stage_screen(player_count,stage):
    while True:
        RenderSystem.display_next_stage_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    result = story_screen(player_count,stage)
                    if result == "main_menu":
                       main_menu()
                       return

def story_screen(player_count,stage):
    story_music=load_story_music(stage)
    music_system_instance.play_music(story_music)
    
    while True:
        RenderSystem.display_story_screen(stage)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    music_system_instance.stop_music(story_music)
                    if(stage != 8):
                        result = game_screen(player_count,stage)
                    else:
                        result = main_menu()
                    if result == "main_menu":
                        main_menu()
                        return
             

def game_screen(player_count, stage):
    yellow = ShipCreation.create_yellow_ship()
    red = None
    
    score_limit = Score.set_score_limit(stage)
    scoreboard = Score(score_limit)

    enemy_ships = []  # List to store enemy ships
    
    if player_count == 2:
        red = ShipCreation.create_red_ship()
    

    movement_system_instance = MovementSystem()
    bullet_system_instance = BulletSystem()
    render_system_instance = RenderSystem()
    
    game_music=load_stage_music(stage)
    music_system_instance.play_music(game_music)
    
    

    
    background = render_system_instance.background_render(stage,WIDTH,HEIGHT)
    
    last_bullet_time = 0
    last_bullet_time_2 = 0
    
    if stage == 7:
        boss=ShipCreation.create_boss_enemy_ship()
        enemy_ships.append(boss)


    load_explosion_images()
    explosions=[]

    
    last_asteroid_spawn_time = 0 #last spawn time of asteroid


    last_spawn_time_green_ships = 0  # Variable to track the last spawn time of green enemy ship
    last_spawn_time_orange_ships = 0
    last_spawn_time_purple_ships = 0
    last_spawn_time_blue_ships = 0
    last_spawn_time_brown_ships = 0


    last_bullet_time_green_ship = 0 
    last_bullet_time_orange_ship = 0
    last_bullet_time_purple_ship = 0
    last_bullet_time_blue_ship = 0
    last_bullet_time_brown_ship = 0
    last_bullet_time_white_ship = 0

    
    
    pause_pressed = False
    game_paused = False

    

    font = pygame.font.Font(None, 24)  # Load a font
    text_display_duration= 5000  # In milliseconds

    prev_score=scoreboard.score
    

    score_text = font.render("Score: " + str(scoreboard.score), True, (255, 255, 255))
    score_rect = score_text.get_rect(midtop=(WIDTH // 2, 10))

    prev_yellow_health = yellow.health
    prev_red_health = red.health if player_count == 2 else None

    
    yellow_health_text = font.render("Yellow Health: " + str(yellow.health), True, (255, 255, 255))
    
    red_health_text = None 

    if player_count == 2:
        red_health_text = font.render("Red Health: " + str(red.health), True, (255, 255, 255))

    run = True
    

    clock = pygame.time.Clock() # reset clock

    
    pause_duration = 0
    game_start_time = pygame.time.get_ticks()
    current_time = pygame.time.get_ticks() - pause_duration - game_start_time
    
    last_score_change = pygame.time.get_ticks() - pause_duration - game_start_time

    last_yellow_health_change = pygame.time.get_ticks() - pause_duration - game_start_time

    last_red_health_change = pygame.time.get_ticks() - pause_duration - game_start_time if player_count == 2 else None


    

    
    
    while run:
        clock.tick(FPS)
        
        
        if scoreboard.has_score_limit_reached():
            next_stage_screen(player_count,stage + 1)
            run =False
            
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not pause_pressed and not game_paused:#in game screen is running we are pressing spacebar to shoot
                        pass
                    else: #press spacebar to continue game
                        game_paused = False
                        result = pause_menu(game_music)
                        if result == "main_menu":
                            #never reached
                            return "main_menu"
                elif event.key == pygame.K_p:
                    if not pause_pressed and not game_paused:#game pause
                        pause_pressed = True
                        game_paused = True
                        
                        
                        pause_start_time=pygame.time.get_ticks()
                        result = pause_menu(game_music)
                        if result == "resume_game":
                            pause_pressed = False
                            game_paused = False
                            result = None
                            
                        elif result == "main_menu":
                            music_system_instance.stop_music(game_music)
                            music_system_instance.play_music("main_menu_music")

                            return "main_menu"

        if game_paused:
            
            game_paused = False
            pause_pressed = False
            result = None
            pause_end_time=pygame.time.get_ticks()
            pause_duration += pause_end_time - pause_start_time
            

        keys_pressed = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks() - pause_duration - game_start_time
              
        #print(pause_duration)
        #print(current_time)

        results = create_ships(enemy_ships, pause_duration, game_start_time, stage, last_spawn_time_green_ships, last_asteroid_spawn_time, last_spawn_time_orange_ships,
                       last_spawn_time_purple_ships, last_spawn_time_blue_ships, last_spawn_time_brown_ships)
        (
                last_bullet_time_green_ship,
                last_bullet_time_orange_ship,
                last_bullet_time_purple_ship,
                last_bullet_time_blue_ship,
                last_bullet_time_brown_ship,
                last_bullet_time_white_ship,
            ) = bullet_system_instance.auto_fire(
                enemy_ships,
                pause_duration,
                game_start_time,
                last_bullet_time_green_ship,
                last_bullet_time_orange_ship,
                last_bullet_time_purple_ship,
                last_bullet_time_blue_ship,
                last_bullet_time_brown_ship,
                last_bullet_time_white_ship,
            )

        if stage == 1:
            last_spawn_time_green_ships = results[0]
            last_asteroid_spawn_time = results[1]

        elif stage == 2:
            last_spawn_time_green_ships = results[0]
            last_spawn_time_orange_ships = results[1]
        elif stage == 3:
            last_spawn_time_green_ships = results[0]
            last_spawn_time_orange_ships = results[1]
            last_spawn_time_purple_ships = results[2]
        elif stage == 4:
            last_spawn_time_orange_ships = results[0]
            last_spawn_time_purple_ships = results[1]
            last_spawn_time_blue_ships = results[2]
        elif stage == 5:
            last_spawn_time_orange_ships = results[0]
            last_spawn_time_purple_ships = results[1]
            last_spawn_time_blue_ships = results[2]
            last_spawn_time_brown_ships = results[3]
        elif stage == 6:
            last_spawn_time_purple_ships = results[0]
            last_spawn_time_blue_ships = results[1]
            last_spawn_time_brown_ships = results[2]
        #elif stage == 7:
         #   last_asteroid_spawn_time= results[0]
        elif stage == 0:
            last_asteroid_spawn_time = results[0]



        movement_system_instance.move_enemy_ships(enemy_ships, WIDTH)  # Move all enemy ships
        
        
        last_bullet_time, last_bullet_time_2 = \
            bullet_system_instance.fire_bullets(yellow, red, player_count, last_bullet_time, last_bullet_time_2,pause_duration,game_start_time,stage)
        update_game_state(yellow, red, enemy_ships, player_count, keys_pressed, movement_system_instance, 
                          bullet_system_instance, render_system_instance, background,scoreboard,explosions)
        
        enemy_ships = [ship for ship in enemy_ships if ship.alive]#keep enemy_ship list from growing large and slowing game down

        if(player_count==1):
            yellow_health_text, last_yellow_health_change, prev_yellow_health = \
                render_system_instance.update_health_text(current_time, yellow, red, prev_yellow_health, prev_red_health, font,
                            last_yellow_health_change,last_red_health_change,yellow_health_text,red_health_text,player_count)
            
            score_text, last_score_change, prev_score = \
                render_system_instance.render_score(scoreboard, font,prev_score,
                                          last_score_change,current_time,score_text) 

        else:
            yellow_health_text, last_yellow_health_change, prev_yellow_health, red_health_text, last_red_health_change, prev_red_health = \
                render_system_instance.update_health_text(current_time, yellow, red, prev_yellow_health, prev_red_health, font,
                            last_yellow_health_change,last_red_health_change,yellow_health_text, red_health_text, player_count)
            score_text, last_score_change, prev_score = \
                render_system_instance.render_score(scoreboard, font,prev_score,last_score_change,current_time,score_text) 


        if current_time - last_score_change < text_display_duration:
            WIN.blit(score_text, score_rect)


        
        if current_time - last_yellow_health_change < text_display_duration:
            WIN.blit(yellow_health_text, (10, 10))

        if player_count == 2 and current_time - last_red_health_change < text_display_duration:  
            WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
        if stage == 0:
            render_system_instance.display_tutorial_instructions(player_count)

        
    
        pygame.display.flip()
        '''
        # Create an explosion at (x, y) and add it to the list
        explosion = Explosion(200, 200)
        explosions.append(explosion)

        

        for explosion in explosions:
            explosion.update()
            explosion.draw(background)
            

          

        # Update the game display
        pygame.display.update()
        
        '''
        
       
        clock.tick(FPS)


def main():
    pygame.init()
    main_menu()
    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    main()