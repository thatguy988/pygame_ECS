import pygame
import os

WIDTH, HEIGHT = 1400, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

class RenderSystem:
    @staticmethod
    def render(entity, surface):
        if entity.alive:
            if hasattr(entity, 'image'):
                surface.blit(entity.image, (entity.position.x, entity.position.y))
   


    def update_health_text(current_time, yellow, red, prev_yellow_health, prev_red_health, font,
                       last_yellow_health_change,last_red_health_change,yellow_health_text,red_health_text,player_count):
        if yellow.health != prev_yellow_health:
            yellow_health_text = font.render("Yellow Health: " + str(yellow.health), True, (255, 255, 255))
            prev_yellow_health = yellow.health
            last_yellow_health_change = current_time

        if red and red.health != prev_red_health:
            red_health_text = font.render("Red Health: " + str(red.health), True, (255, 255, 255))
            prev_red_health = red.health
            last_red_health_change = current_time

        if player_count == 1 :
            return yellow_health_text, last_yellow_health_change, prev_yellow_health
        else:
            return yellow_health_text, last_yellow_health_change, prev_yellow_health, red_health_text, last_red_health_change, prev_red_health
        
    def background_render(stage,WIDTH,HEIGHT):
        if(stage == 1):
            background = pygame.image.load(os.path.join('assets', 'space.png'))
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            return background
        elif(stage == 2):
            background = False
            return background
        

    def draw_window(entities, bullet_system, background, color):
        WIN.blit(background, (0, 0))
        
        for entity in entities:
            RenderSystem.render(entity, WIN)
        
        bullet_system.render_bullets(WIN, color)
        #asteroid.draw(WIN) 

    pygame.display.update()


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

    def render_game_over_screen():
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