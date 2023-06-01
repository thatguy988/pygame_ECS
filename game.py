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
GREEN_ENEMY_SHIP_VEL = 3
ASTEROID_VEL = 2
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
                game_screen(1, stage)  # Start game with 1 player
            elif player_count == 2:
                stage = select_stage_screen()  # Select the stage
                if(stage == 0):
                    continue
                game_screen(2, stage)  # Start game with 2 players

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


def update_game_state(yellow, red, enemy_ships, player_count, keys_pressed, movement_system, bullet_system_instance,background,asteroids):

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
        bullet_system_instance.handle_ship_asteroid_collision(red, asteroids, WIDTH, HEIGHT)
        bullet_system_instance.handle_enemyship_ship_collision(red, enemy_ships, WIDTH, HEIGHT)
    else:
        bullet_system_instance.handle_ship_asteroid_collision(yellow, asteroids, WIDTH, HEIGHT)
        bullet_system_instance.handle_enemyship_ship_collision(yellow, enemy_ships, WIDTH, HEIGHT)
    #bullet_system_instance.handle_enemy_asteroid_collision(enemy_ships,asteroids,WIDTH,HEIGHT)
    bullet_system_instance.update_bullets_and_check_collisions(enemy_ships, WIDTH, yellow, red, player_count,WIN,BLACK,HEIGHT,asteroids)

    if not yellow.alive and player_count == 1:
            game_over_screen()

    if player_count == 2:
        if not red.alive and not yellow.alive:
                game_over_screen()

def game_over_screen():
    while True:
        RenderSystem.render_game_over_screen()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_menu()
                    return # Return to the main menu


def game_screen(player_count, stage):
    yellow = create_yellow_ship()
    red = None
    #enemy_ship = create_enemy_ship()

    enemy_ships = []  # List to store enemy ships
    asteroids = []
    #asteroid = create_asteroid()

    

    if player_count == 2:
        red = create_red_ship()
    
    movement_system = MovementSystem()
    bullet_system_instance = BulletSystem()
    
    background = RenderSystem.background_render(stage,WIDTH,HEIGHT)
    

    clock = pygame.time.Clock()

    last_bullet_time = 0
    last_bullet_time_2 = 0
    last_bullet_time_enemy_ship = 0
    


    last_asteroid_spawn_time = 0
    asteroid_spawn_rate = 3000

    last_spawn_time = 0  # Variable to track the last spawn time
    spawn_rate = 5000  # Time interval (in milliseconds) between enemy ship spawns
    
    pause_pressed = False
    game_paused = False

    font = pygame.font.Font(None, 24)  # Load a font
    text_display_duration= 5000  # In milliseconds


    prev_yellow_health = yellow.health
    prev_red_health = red.health if player_count == 2 else None

    last_yellow_health_change = pygame.time.get_ticks()
    last_red_health_change = pygame.time.get_ticks() if player_count == 2 else None
    
    yellow_health_text = font.render("Yellow Health: " + str(yellow.health), True, (255, 255, 255))
    
    red_health_text = None 

    if player_count == 2:
        red_health_text = font.render("Red Health: " + str(red.health), True, (255, 255, 255))

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not pause_pressed and not game_paused:
                        pass
                    else:
                        game_paused = False
                        result = pause_menu()
                        if result == "main_menu":
                            return "main_menu"
                elif event.key == pygame.K_p:
                    if not pause_pressed and not game_paused:
                        pause_pressed = True
                        game_paused = True
                        result = pause_menu()
                        if result == "resume_game":
                            pause_pressed = False
                            game_paused = False
                            result = None
                            return "resume_game"
                        elif result == "main_menu":
                            return "main_menu"

        if game_paused:
            game_paused = False
            pause_pressed = False
            result = None
        
        keys_pressed = pygame.key.get_pressed()

        

        last_spawn_time = spawn_enemy_ships(enemy_ships, spawn_rate, last_spawn_time,stage)
        last_asteroid_spawn_time = spawn_asteroids(asteroids, asteroid_spawn_rate, last_asteroid_spawn_time,stage)
        last_bullet_time, last_bullet_time_2 = \
            bullet_system_instance.fire_bullet(yellow, red, player_count, last_bullet_time, last_bullet_time_2)
        update_game_state(yellow, red, enemy_ships, player_count, keys_pressed, movement_system, bullet_system_instance, background,asteroids)

        current_time = pygame.time.get_ticks()
        if(player_count==1):
            yellow_health_text, last_yellow_health_change, prev_yellow_health = \
                RenderSystem.update_health_text(current_time, yellow, red, prev_yellow_health, prev_red_health, font,
                            last_yellow_health_change,last_red_health_change,yellow_health_text,red_health_text,player_count)
        else:
            yellow_health_text, last_yellow_health_change, prev_yellow_health, red_health_text, last_red_health_change, prev_red_health = \
                RenderSystem.update_health_text(current_time, yellow, red, prev_yellow_health, prev_red_health, font,
                            last_yellow_health_change,last_red_health_change,yellow_health_text, red_health_text, player_count)
        
        if current_time - last_yellow_health_change < text_display_duration:
            WIN.blit(yellow_health_text, (10, 10))

        if player_count == 2 and current_time - last_red_health_change < text_display_duration:  
            WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    
        pygame.display.flip()
        
        movement_system.move_asteroid(asteroids, WIDTH, ASTEROID_VEL)

        movement_system.move_enemy_ships(enemy_ships, WIDTH, GREEN_ENEMY_SHIP_VEL)  # Move all enemy ships
        last_bullet_time_enemy_ship = bullet_system_instance.auto_fire(enemy_ships, last_bullet_time_enemy_ship)  # Fire bullets from all enemy ships
        
        clock.tick(FPS)

    pygame.quit()


def main():
    pygame.init()
    main_menu()

    while True:
        result = game_screen()
        if result == "main_menu":
            main_menu()



if __name__ == "__main__":
    main()