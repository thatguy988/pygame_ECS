import pygame
import sys
import os
from components.position import PositionComponent
from systems.movement import MovementSystem
from systems.render import RenderSystem
from systems.bullet_system import BulletSystem
from components.bullet import Bullet

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)    

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

FPS = 120
VEL = 4

class Entity:
    def __init__(self, *components):
        self.components = list(components)

    def get_component(self, component_type):
        for component in self.components:
            if isinstance(component, component_type):
                return component
        return None


def draw_window(entities, bullet_system, background, color):
    WIN.blit(background, (0, 0))  # Draw the background image

    for entity in entities:
        position_component = entity.get_component(PositionComponent)
        if position_component:
            x = position_component.x
            y = position_component.y
            RenderSystem.render(entity, WIN, x, y)  # Pass x and y as arguments

    bullet_system.render_bullets(WIN, color)
    pygame.display.update()

def display_menu(selected_option):
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
            cursor_image = pygame.transform.scale(cursor_image, (50, 30))  # Change size of cursor ship image
            cursor_image = pygame.transform.rotate(cursor_image, 90)  # Change rotation of cursor ship image
            cursor_rect = cursor_image.get_rect()
            cursor_rect.center = (WIDTH // 2 - 100, option_y)
            WIN.blit(cursor_image, cursor_rect)
        
        option_y += option_spacing
    
    pygame.display.update()


def handle_menu_events(selected_option):
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
                    # Start Game
                    return "start_game"
                elif selected_option == 1:
                    # Options
                    return "tutorial"
                elif selected_option == 2:
                    # Quit
                    pygame.quit()
                    sys.exit()

    return selected_option


def main_menu():
    selected_option = 0  # Default selected option
    while True:
        display_menu(selected_option)
        selected_option = handle_menu_events(selected_option)
        if selected_option == "start_game":
            game_screen()
            selected_option = 0  # Reset the selected option when returning from the game screen
        elif selected_option =="tutorial":
            tutorial_screen()
            selected_option = 0
                
    
def pause_menu():
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
            cursor_rect.center = (WIDTH // 2 - 100, option_y)
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


def game_screen():
    #create spaceship player
    yellow = Entity(PositionComponent(100, 300))
    yellow.image = pygame.transform.rotate(
        pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'spaceship_yellow.png')),
            (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        ),
        90
    )
    yellow.position = yellow.get_component(PositionComponent)

    movement_system = MovementSystem()
    bullet_system_instance = BulletSystem()

    background = pygame.image.load(os.path.join('assets', 'Purple_Nebula_Game.png'))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    space_pressed = False
    last_bullet_time = 0
    pause_pressed = False
    result = None
    game_paused = False

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not pause_pressed:
                        if not game_paused:
                            space_pressed = True
                        else:
                            game_paused = False
                            result = pause_menu()
                            if result == "main_menu":
                                return "main_menu"
                    else:
                        pause_pressed = False
                elif event.key == pygame.K_p:
                    if not pause_pressed:
                        if not game_paused:
                            pause_pressed = True
                            game_paused = True
                            result = pause_menu()
                            if result == "resume_game":
                                pause_pressed = False
                                game_paused = False
                                result = None
                            elif result == "main_menu":
                                return "main_menu"
                                # Exit the game loop and return to the main menu

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    space_pressed = False
                    last_bullet_time = 0

        if game_paused:
            continue

        if space_pressed:
            current_time = pygame.time.get_ticks()
            time_since_last_bullet = current_time - last_bullet_time

            if time_since_last_bullet >= 100:
                bullet_system_instance.create_bullet(
                    yellow.position.x + SPACESHIP_WIDTH, yellow.position.y + SPACESHIP_HEIGHT // 2, 5
                )
                last_bullet_time = current_time

        keys_pressed = pygame.key.get_pressed()
        movement_system.move(
            yellow, keys_pressed, WIDTH, HEIGHT, VEL, SPACESHIP_WIDTH, SPACESHIP_HEIGHT
        )
        draw_window([yellow], bullet_system_instance, background, BLACK)
        bullet_system_instance.update(WIDTH, BLACK, WIN)

        clock.tick(FPS)

    pygame.quit()

def tutorial_screen():
    pygame.font.init()  # Initialize the font module
    font = pygame.font.Font(None, 30)
    text_color = (255, 255, 255)

    # Create spaceship player
    yellow = Entity(PositionComponent(100, 300))
    yellow.image = pygame.transform.rotate(
        pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'spaceship_yellow.png')),
            (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        ),
        90
    )
    yellow.position = yellow.get_component(PositionComponent)

    movement_system = MovementSystem()
    bullet_system_instance = BulletSystem()

    background = pygame.image.load(os.path.join('assets', 'space.png'))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    space_pressed = False
    last_bullet_time = 0
    pause_pressed = False
    result = None
    game_paused = False



    # Create a separate buffer surface
    buffer_surface = pygame.Surface((WIDTH, HEIGHT))

    # Render and display the text
    controls_text = font.render("Controls: W - Move Up, S - Move Down, A - Move Left, D - Move Right", True, text_color)
    fire_text = font.render("Spacebar - Fire", True, text_color)
    pause_text = font.render("P - Pause the game", True, text_color)
    

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not pause_pressed:
                        if not game_paused:
                            space_pressed = True
                        else:
                            game_paused = False
                            result = pause_menu()
                            if result == "main_menu":
                                return "main_menu"
                    else:
                        pause_pressed = False
                elif event.key == pygame.K_p:
                    if not pause_pressed:
                        if not game_paused:
                            pause_pressed = True
                            game_paused = True
                            result = pause_menu()
                            if result == "resume_game":
                                pause_pressed = False
                                game_paused = False
                                result = None
                            elif result == "main_menu":
                                return "main_menu"
                                # Exit the game loop and return to the main menu

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    space_pressed = False
                    last_bullet_time = 0

        if game_paused:
            continue

        if space_pressed:
            current_time = pygame.time.get_ticks()
            time_since_last_bullet = current_time - last_bullet_time

            if time_since_last_bullet >= 100:
                bullet_system_instance.create_bullet(
                    yellow.position.x + SPACESHIP_WIDTH, yellow.position.y + SPACESHIP_HEIGHT // 2, 5
                )
                last_bullet_time = current_time

        keys_pressed = pygame.key.get_pressed()
        movement_system.move(
            yellow, keys_pressed, WIDTH, HEIGHT, VEL, SPACESHIP_WIDTH, SPACESHIP_HEIGHT
        )
        bullet_system_instance.update(WIDTH, BLACK, buffer_surface)

        # Clear the buffer surface
        buffer_surface.fill(BLACK)

        # Draw the background and spaceship on the buffer surface
        buffer_surface.blit(background, (0, 0))
        buffer_surface.blit(yellow.image, (yellow.position.x, yellow.position.y))

        # Draw the text surfaces on the buffer surface
        buffer_surface.blit(controls_text, (10, 10))
        buffer_surface.blit(fire_text, (10, 40))
        buffer_surface.blit(pause_text, (10, 70))

        # Copy the buffer surface to the window surface
        WIN.blit(buffer_surface, (0, 0))

        
        

        '''
        draw_window([yellow], bullet_system_instance, background, BLACK)
        WIN.blit(background, (0, 0))
        WIN.blit(yellow.image, (yellow.position.x, yellow.position.y))
        WIN.blit(controls_text, (10, 10))
        WIN.blit(fire_text, (10, 40))
        WIN.blit(pause_text, (10, 70))
        bullet_system_instance.update(WIDTH, BLACK, WIN)
        '''
        

        

        pygame.display.update()


       

        clock.tick(FPS)

    pygame.quit()


def main():
    pygame.init()
    main_menu()

    while True:
        result = game_screen()
        if result == "main_menu":
            main_menu()

    pygame.quit()

if __name__ == "__main__":
    main()