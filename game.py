import pygame
import sys
import os


from systems.movement import MovementSystem
from systems.render import RenderSystem
from systems.bullet_system import BulletSystem
from systems.ship_system import spawn_enemy_ships,spawn_asteroids
from systems.menu_input_system import MenuHandling

from components.explosion import Explosion
from components.dimension import Dimensions
from components.score import Score
from components.ship import create_yellow_ship,create_red_ship, create_asteroid

WIDTH, HEIGHT = 1400, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)    
RED = (255, 0, 0)


FPS = 120
VEL = 4

ENEMY_SHIP_SPAWN_RATE = 120  # Adjust the spawn rate as needed



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
                    selected_option = (selected_option - 1) % 7  # 7 for 7 options
                elif event.key == pygame.K_s:
                    selected_option = (selected_option + 1) % 7  
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
                        return 0 # back


def main_menu():
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
                print("hello from main menu method")
                story_screen(player_count,stage)
                #game_screen(1, stage)  # Start game with 1 player
            elif player_count == 2:
                stage = select_stage_screen()  # Select the stage
                if(stage == 0):
                    continue
                story_screen(player_count,stage)
                #game_screen(2, stage)  # Start game with 2 players

            selected_option = 0  # Reset the selected option for when player goes back to main menu
        elif selected_option == "tutorial":
            #tutorial_screen()
            selected_option = 0


def pause_menu():#main loop for pause menu
    selected_option = 0  # Default selected option
    while True:
        RenderSystem.display_pause_menu(selected_option)
        selected_option = MenuHandling.handle_pause_menu_events(selected_option)
        if selected_option == "resume_game":
            return  # Resume the game
        elif selected_option == "main_menu":
            return "main_menu"  # Go back to the main menu


def update_game_state(yellow, red, enemy_ships, player_count, keys_pressed, movement_system, bullet_system_instance,background,asteroids,scoreboard,font):

    if player_count >= 1:
        movement_system.move_player1(
            yellow, keys_pressed, WIDTH, HEIGHT, VEL, yellow.width, yellow.height
        )

    if player_count == 2:
        movement_system.move_player2(
            red, keys_pressed, WIDTH, HEIGHT, VEL, yellow.width, yellow.height
        )

    if player_count == 2:
        RenderSystem.draw_window([yellow, red] + enemy_ships + asteroids, bullet_system_instance, background, WHITE)
    else:
        RenderSystem.draw_window([yellow] + enemy_ships + asteroids,bullet_system_instance, background, WHITE)
    if player_count == 2:
        bullet_system_instance.handle_ship_asteroid_collision(red, asteroids, WIDTH, HEIGHT,scoreboard)
        bullet_system_instance.handle_enemyship_ship_collision(red, enemy_ships, WIDTH, HEIGHT,scoreboard)
    else:
        bullet_system_instance.handle_ship_asteroid_collision(yellow, asteroids, WIDTH, HEIGHT,scoreboard)
        bullet_system_instance.handle_enemyship_ship_collision(yellow, enemy_ships, WIDTH, HEIGHT,scoreboard)
    #bullet_system_instance.handle_enemy_asteroid_collision(enemy_ships,asteroids,WIDTH,HEIGHT)
    bullet_system_instance.update_bullets_and_check_collisions(enemy_ships, WIDTH, yellow, red, player_count,WIN,BLACK,HEIGHT,asteroids,scoreboard)

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
                    return # Return to the main menu


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
    while True:
        RenderSystem.display_story_screen(stage)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    result = game_screen(player_count,stage)
                    if result == "main_menu":
                        main_menu()
                        return
             

def game_screen(player_count, stage):
    yellow = create_yellow_ship()
    red = None
    #enemy_ship = create_enemy_ship()
    score_limit = Score.set_score_limit(stage)
    scoreboard = Score(score_limit)

    enemy_ships = []  # List to store enemy ships
    asteroids = [] # List to store asteroids
    #asteroid = create_asteroid()


    if player_count == 2:
        red = create_red_ship()
    
    movement_system = MovementSystem()
    bullet_system_instance = BulletSystem()
    
    background = RenderSystem.background_render(stage,WIDTH,HEIGHT)
    
    

    last_bullet_time = 0
    last_bullet_time_2 = 0
    last_bullet_time_enemy_ship = 0
    
    last_asteroid_spawn_time = 0 #last spawn time of asteroid
    asteroid_spawn_rate = 3000# spawn time interval

    last_spawn_time = 0  # Variable to track the last spawn time of green enemy ship
    spawn_rate = 5000  # Time interval (in milliseconds) between enemy ship spawns
    
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
            print("Returning to the main menu...")
            run = False
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
                        result = pause_menu()
                        if result == "main_menu":
                            #never reached
                            return "main_menu"
                elif event.key == pygame.K_p:
                    if not pause_pressed and not game_paused:#game pause
                        pause_pressed = True
                        game_paused = True
                        pause_start_time=pygame.time.get_ticks()
                        result = pause_menu()
                        if result == "resume_game":
                            pause_pressed = False
                            game_paused = False
                            result = None
                            
                        elif result == "main_menu":
                            print("hello2")
                            
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

        


        last_spawn_time = spawn_enemy_ships(enemy_ships, spawn_rate, last_spawn_time,stage, pause_duration)
        last_asteroid_spawn_time = spawn_asteroids(asteroids, asteroid_spawn_rate, last_asteroid_spawn_time,stage, pause_duration)
        last_bullet_time, last_bullet_time_2 = \
            bullet_system_instance.fire_bullet(yellow, red, player_count, last_bullet_time, last_bullet_time_2,pause_duration)
        update_game_state(yellow, red, enemy_ships, player_count, keys_pressed, movement_system, 
                          bullet_system_instance, background,asteroids,scoreboard,font)

        #current_time = pygame.time.get_ticks()
        


        if(player_count==1):
            yellow_health_text, last_yellow_health_change, prev_yellow_health = \
                RenderSystem.update_health_text(current_time, yellow, red, prev_yellow_health, prev_red_health, font,
                            last_yellow_health_change,last_red_health_change,yellow_health_text,red_health_text,player_count)
            
            score_text, last_score_change, prev_score = \
                RenderSystem.render_score(scoreboard, font,prev_score,
                                          last_score_change,current_time,score_text) 

        else:
            yellow_health_text, last_yellow_health_change, prev_yellow_health, red_health_text, last_red_health_change, prev_red_health = \
                RenderSystem.update_health_text(current_time, yellow, red, prev_yellow_health, prev_red_health, font,
                            last_yellow_health_change,last_red_health_change,yellow_health_text, red_health_text, player_count)
            score_text, last_score_change, prev_score = \
                RenderSystem.render_score(scoreboard, font,prev_score,last_score_change,current_time,score_text) 


        if current_time - last_score_change < text_display_duration:
            WIN.blit(score_text, score_rect)


        
        if current_time - last_yellow_health_change < text_display_duration:
            WIN.blit(yellow_health_text, (10, 10))

        if player_count == 2 and current_time - last_red_health_change < text_display_duration:  
            WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    
        pygame.display.flip()
        
        movement_system.move_asteroid(asteroids, WIDTH)

        movement_system.move_enemy_ships(enemy_ships, WIDTH)  # Move all enemy ships
        last_bullet_time_enemy_ship = bullet_system_instance.auto_fire(enemy_ships, last_bullet_time_enemy_ship,pause_duration)  # Fire bullets from all enemy ships
        
        clock.tick(FPS)

    



def main():
    pygame.init()
    main_menu()
    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    main()