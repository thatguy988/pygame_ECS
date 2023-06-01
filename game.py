import pygame
import sys
import os
import random

from systems.movement import MovementSystem
from systems.render import RenderSystem
from systems.bullet_system import BulletSystem
from systems.ship import create_yellow_ship, create_red_ship,create_enemy_ship, spawn_enemy_ships


from components.explosion import Explosion
from components.dimension import Dimensions




WIDTH, HEIGHT = 1400, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)    
RED = (255, 0, 0)
GREY = (128, 128, 128)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

FPS = 120
VEL = 4
GREEN_ENEMY_SHIP_VEL = 4
ENEMY_SHIP_SPAWN_RATE = 120  # Adjust the spawn rate as needed



def draw_window(entities, bullet_system, background, color):
    WIN.blit(background, (0, 0))
    
    for entity in entities:
        RenderSystem.render(entity, WIN)
    
    
    bullet_system.render_bullets(WIN, color)
    

    
    pygame.display.update()



def select_players_screen():
    selected_option = 0
    while True:
        display_select_players_screen(selected_option)
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
                        
def display_select_players_screen(selected_option):
    WIN.fill((0, 0, 0))  # Clear screen

    # Render the title text
    title_font = pygame.font.SysFont(None, 60)
    title_text = title_font.render("Select Players", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    WIN.blit(title_text, title_rect)

    # Render the menu options
    menu_font = pygame.font.SysFont(None, 40)
    options = ["1 Player", "2 Players", "Back"]
    option_y = HEIGHT // 2
    option_spacing = 60

    for i, option in enumerate(options):
        option_text = menu_font.render(option, True, (255, 255, 255))
        option_rect = option_text.get_rect(center=(WIDTH // 2, option_y))
        WIN.blit(option_text, option_rect)

        # Display cursor image for selected option
        if i == selected_option:
            cursor_image = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))
            cursor_image = pygame.transform.scale(cursor_image, (50, 30))
            cursor_image = pygame.transform.rotate(cursor_image, 90)
            cursor_rect = cursor_image.get_rect() 
                
            if option == "1 Player":
                cursor_rect.center = (WIDTH // 2 - 80, option_y)  # Cursor position for "Resume Game"
            elif option == "2 Players":
                cursor_rect.center = (WIDTH // 2 - 100, option_y)  # Cursor position for other options
            elif option == "Back":
                cursor_rect.center = (WIDTH // 2 - 60, option_y) # Cursor position for "Back"
                
            WIN.blit(cursor_image, cursor_rect)

        option_y += option_spacing
        
    pygame.display.update()

def select_stage_screen():
    selected_option = 0
    while True:
        display_select_stage_screen(selected_option)
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
                    #return selected_option  # Return the selected stage


def display_select_stage_screen(selected_option):
    WIN.fill((0, 0, 0))  #clear

    # Render the title text
    title_font = pygame.font.SysFont(None, 60)
    title_text = title_font.render("Select Stage", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 12))
    WIN.blit(title_text, title_rect)

    # Render the stage options
    menu_font = pygame.font.SysFont(None, 40)
    stages = ["Stage 1", "Stage 2", "Stage 3", "Stage 4", "Stage 5", "Stage 6", "Back"]
    option_y = HEIGHT // 5
    option_spacing = 60

    for i, stage in enumerate(stages):
        stage_text = menu_font.render(stage, True, (255, 255, 255))
        stage_rect = stage_text.get_rect(center=(WIDTH // 2, option_y))
        WIN.blit(stage_text, stage_rect)

        # Display cursor image for selected option
        if i == selected_option:
            cursor_image = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))
            cursor_image = pygame.transform.scale(cursor_image, (50, 30))
            cursor_image = pygame.transform.rotate(cursor_image, 90)
            cursor_rect = cursor_image.get_rect()


            cursor_rect.center = (WIDTH // 2 - 100, option_y)  # Cursor position for other options

            WIN.blit(cursor_image, cursor_rect)

        option_y += option_spacing

    pygame.display.update()


def main_menu():
    selected_option = 0  # Default selected option
    while True:
        display_menu(selected_option)
        selected_option = handle_menu_events(selected_option)
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

def display_menu(selected_option): #render and display main_menu
    # Clear the screen
    WIN.fill((0, 0, 0))
    
    # Render the title text
    title_font = pygame.font.SysFont(None, 60)
    title_text = title_font.render("Main Menu", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    WIN.blit(title_text, title_rect)
    
    # Render the menu options
    menu_font = pygame.font.SysFont(None, 40)
    options = ["Start Game", "Tutorial", "Quit"]
    option_y = HEIGHT // 2
    option_spacing = 60
    
    for i, option in enumerate(options):
        option_text = menu_font.render(option, True, (255, 255, 255))
        option_rect = option_text.get_rect(center=(WIDTH // 2, option_y))
        WIN.blit(option_text, option_rect)
        

       # Display cursor image for selected option
        if i == selected_option:
            cursor_image = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))
            cursor_image = pygame.transform.scale(cursor_image, (50, 30))
            cursor_image = pygame.transform.rotate(cursor_image, 90)
            cursor_rect = cursor_image.get_rect() 
            
            if option == "Start Game":
                cursor_rect.center = (WIDTH // 2 - 100, option_y)  # Cursor position for "Resume Game"
            elif option == "Tutorial":
                cursor_rect.center = (WIDTH // 2 - 80, option_y)  # Cursor position for "Tutorial"
            elif option == "Quit":
                cursor_rect.center = (WIDTH // 2 - 60, option_y) # Cursor position for "Quit"

            WIN.blit(cursor_image, cursor_rect)

        option_y += option_spacing #space out main menu options vertically
    
    pygame.display.update()


def handle_menu_events(selected_option): #responsible for handling the user input events related to the main menu
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
                    return "start_game"
                elif selected_option == 1:
                    return "tutorial"
                elif selected_option == 2:
                    pygame.quit()
                    sys.exit()

    return selected_option





def pause_menu():#main loop for pause menu
    selected_option = 0  # Default selected option
    while True:
        display_pause_menu(selected_option)
        selected_option = handle_pause_menu_events(selected_option)
        if selected_option == "resume_game":
            return  # Resume the game
        elif selected_option == "main_menu":
            return "main_menu"  # Go back to the main menu




def display_pause_menu(selected_option):
    # Clear the screen
    WIN.fill((0, 0, 0))
    
    # Render the title text
    title_font = pygame.font.SysFont(None, 60)
    title_text = title_font.render("Pause Menu", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    WIN.blit(title_text, title_rect)
    
    # Render the menu options
    menu_font = pygame.font.SysFont(None, 40)
    options = ["Resume Game", "Main Menu"]
    option_y = HEIGHT // 2
    option_spacing = 60
    
    for i, option in enumerate(options):
        option_text = menu_font.render(option, True, (255, 255, 255))
        option_rect = option_text.get_rect(center=(WIDTH // 2, option_y))
        WIN.blit(option_text, option_rect)
        
        # Display cursor image for selected option
        if i == selected_option:
            cursor_image = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))
            cursor_image = pygame.transform.scale(cursor_image, (50, 30))
            cursor_image = pygame.transform.rotate(cursor_image, 90)
            cursor_rect = cursor_image.get_rect() 
            
            if option == "Resume Game":
                cursor_rect.center = (WIDTH // 2 - 120, option_y)  # Cursor position for "Resume Game"
            elif option == "Main Menu":
                cursor_rect.center = (WIDTH // 2 - 100, option_y)  # Cursor position for other options
            
            WIN.blit(cursor_image, cursor_rect)

        option_y += option_spacing
    
    pygame.display.update()


def handle_pause_menu_events(selected_option):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                selected_option = (selected_option - 1) % 2  # Move up in the options list
            elif event.key == pygame.K_s:
                selected_option = (selected_option + 1) % 2  # Move down in the options list
            elif event.key == pygame.K_SPACE:
                if selected_option == 0:
                    # Resume Game
                    return "resume_game"
                elif selected_option == 1:
                    # Main Menu
                    return "main_menu"

    return selected_option


def update_game_state(yellow, red, enemy_ships, player_count, keys_pressed, movement_system, bullet_system_instance,background):

    if player_count >= 1:
        movement_system.move_player1(
            yellow, keys_pressed, WIDTH, HEIGHT, VEL, SPACESHIP_WIDTH, SPACESHIP_HEIGHT
        )

    if player_count == 2:
        movement_system.move_player2(
            red, keys_pressed, WIDTH, HEIGHT, VEL, SPACESHIP_WIDTH, SPACESHIP_HEIGHT
        )

    if player_count == 2:
        #draw_window([yellow, red, enemy_ship], bullet_system_instance, background, WHITE)
        draw_window([yellow, red] + enemy_ships, bullet_system_instance, background, WHITE)
    else:
        #draw_window([yellow,enemy_ship], bullet_system_instance, background, WHITE)
        draw_window([yellow] + enemy_ships,bullet_system_instance, background, WHITE)
        




    bullet_system_instance.update_bullets_and_check_collisions(enemy_ships, WIDTH, yellow, red, player_count,WIN,BLACK,HEIGHT)

    if not yellow.alive and player_count == 1:
            game_over_screen()

    if player_count == 2:
        if not red.alive and not yellow.alive:
                game_over_screen()

def game_over_screen():
    while True:
        WIN.fill((0, 0, 0))  # Clear the screen
        
        # Render the game over message
        game_over_font = pygame.font.SysFont(None, 60)
        game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        WIN.blit(game_over_text, game_over_rect)
        
        # Render the instructions
        instructions_font = pygame.font.SysFont(None, 40)
        instructions_text = instructions_font.render("Press R to return to the main menu", True, (255, 255, 255))
        instructions_rect = instructions_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        WIN.blit(instructions_text, instructions_rect)
        
        pygame.display.update()
        
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


        last_bullet_time, last_bullet_time_2 = \
            bullet_system_instance.fire_bullet(yellow, red, player_count, last_bullet_time, last_bullet_time_2)
        update_game_state(yellow, red, enemy_ships, player_count, keys_pressed, movement_system, bullet_system_instance, background)

        
        
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