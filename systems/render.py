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


    @staticmethod
    def render_score(scoreboard, font,prev_score,last_score_change,current_time,score_text):
        if scoreboard.score != prev_score:
            score_text = font.render("Score: " + str(scoreboard.score), True, (255, 255, 255))
            prev_score = scoreboard.score
            last_score_change = current_time
        return score_text, last_score_change, prev_score,
            
   

    @staticmethod
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
        

    @staticmethod
    def display_tutorial_instructions(player_count):
        
        if player_count == 1:
            
            instructions_font = pygame.font.SysFont(None, 40)
            instructions_text = instructions_font.render("Player 1: Press W A S D to move and press spacebar to shoot", True, (255, 255, 255))
            instructions_rect = instructions_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
            WIN.blit(instructions_text, instructions_rect)

            
            pygame.display.update(instructions_rect)
        else:
            instructions_font = pygame.font.SysFont(None, 40)

            instructions_text1 = instructions_font.render("Player 1: Press W A S D to move and press spacebar to shoot", True, (255, 255, 255))
            instructions_text2 = instructions_font.render("Player 2: Press I J K L to move and press enter to shoot", True, (255, 255, 255))

            instructions_rect1 = instructions_text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
            instructions_rect2 = instructions_text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 140))

            WIN.blit(instructions_text1, instructions_rect1)
            WIN.blit(instructions_text2, instructions_rect2)

            
            pygame.display.update([instructions_rect1, instructions_rect2])




    @staticmethod    
    def background_render(stage,WIDTH,HEIGHT):
        if(stage == 1):
            background = pygame.image.load(os.path.join('assets', 'space.png'))
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            return background
        elif(stage == 2):
            background = pygame.image.load(os.path.join('assets', 'Purple_Nebula_Stage_2.png'))
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            return background
        elif(stage == 3):
            background = pygame.image.load(os.path.join('assets', 'Green_Nebula_Stage_3.png'))
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            return background
        elif(stage == 4):
            background = pygame.image.load(os.path.join('assets', 'Blue_Nebula_Stage_4.png'))
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            return background
        elif(stage == 5):
            background = pygame.image.load(os.path.join('assets', 'Green_Nebula_Stage_5.png'))
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            return background
        elif(stage == 6):
            background = pygame.image.load(os.path.join('assets', 'Purple_Nebula_Stage_6.png'))
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            return background
        elif(stage == 7):
            background = pygame.image.load(os.path.join('assets', 'Purple_Nebula_Boss_Level.png'))
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            return background
        elif(stage == 0):
            background = pygame.image.load(os.path.join('assets', 'Tutorial_Background.png'))
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            return background
        else:
            background = pygame.image.load(os.path.join('assets', 'Starfield_Default.png'))
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))


            return background

        
    @staticmethod
    def draw_window(entities, bullet_system, background, color):
        WIN.blit(background, (0, 0))
        
        for entity in entities:
            RenderSystem.render(entity, WIN)
        
        bullet_system.render_bullets(WIN, color)
        


    pygame.display.update()





    def display_menu(selected_option): #render and display main_menu
        

        # Clear the screen
        WIN.fill((0, 0, 0))
        background = pygame.image.load(os.path.join('assets', 'Starfield_Menu_Background.png'))
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        WIN.blit(background, (0, 0))
        
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
        background = pygame.image.load(os.path.join('assets', 'Starfield_Menu_Background.png'))
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        WIN.blit(background, (0, 0))

        # Render the title text
        title_font = pygame.font.SysFont(None, 60)
        title_text = title_font.render("Select Stage", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 12))
        WIN.blit(title_text, title_rect)

        # Render the stage options
        menu_font = pygame.font.SysFont(None, 40)
        stages = ["Stage 1", "Stage 2", "Stage 3", "Stage 4", "Stage 5", "Stage 6", "Boss Level", "Back"]
        option_y = HEIGHT // 6
        option_spacing = 50

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
        background = pygame.image.load(os.path.join('assets', 'Starfield_Menu_Background.png'))
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        WIN.blit(background, (0, 0))
        
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
        background = pygame.image.load(os.path.join('assets', 'Starfield_Menu_Background.png'))
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        WIN.blit(background, (0, 0))

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

    def display_game_over_screen():
        WIN.fill((0, 0, 0))  # Clear the screen
        background = pygame.image.load(os.path.join('assets', 'Starfield_Menu_Background.png'))
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        WIN.blit(background, (0, 0))
        
        
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

    def display_next_stage_screen():
        WIN.fill((0, 0, 0))  # Clear the screen
        background = pygame.image.load(os.path.join('assets', 'Starfield_Menu_Background.png'))
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        WIN.blit(background, (0, 0))
            
            
        # Render Stage Complete
        game_over_font = pygame.font.SysFont(None, 60)
        game_over_text = game_over_font.render("Stage Complete", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        WIN.blit(game_over_text, game_over_rect)
            
        # Render instructions
        instructions_font = pygame.font.SysFont(None, 40)
        instructions_text = instructions_font.render("Press F to go to next stage", True, (255, 255, 255))
        instructions_rect = instructions_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        WIN.blit(instructions_text, instructions_rect)
            
        pygame.display.update()



    def display_story_screen(stage):
        WIN.fill((0, 0, 0))  # Clear the screen
        background = pygame.image.load(os.path.join('assets', 'cool_pixel_art_background.png'))
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        WIN.blit(background, (0, 0))
            
        story_font = pygame.font.SysFont(None, 60)
        story_rect = story_font.render("", True, (255, 255, 255)).get_rect(center=(WIDTH // 2, HEIGHT // 2))
        instructions_font = pygame.font.SysFont(None, 40)
        instructions_text = instructions_font.render("", True, (255, 255, 255))
        instructions_rect = instructions_text.get_rect(center=(WIDTH // 2 - 175, HEIGHT // 2 + 100)) #adjust instruction position
        instructions_text = instructions_font.render("Press F to go to next stage", True, (255, 255, 255))

        story_rect.centerx = WIDTH // 2 - 280 # Move story_text width
        story_rect.centery = HEIGHT // 2 - 100  # Move story_text height



        if stage == 1:    
            story_text = story_font.render("Stage 1: The Journey Begins", True, (255, 255, 255))
            story_paragraph = "In the year 25XX, the galaxy was in turmoil as a group of space bandits terrorized its inhabitants. Three brave spaceships, piloted by our courageous heroes, rose to the occasion to put an end to their tyranny. Determined and armed with their advanced weaponry, they embarked on their mission, setting a course towards the bandits' home planet."
        elif stage == 2:
            story_text = story_font.render("Stage 2: The New Arsenal", True, (255, 255, 255))
            story_paragraph = "As they progressed through space, our heroes discovered a valuable upgrade for their ships—a cutting-edge weapon system that unleashed a barrage of double bullets. With this powerful new arsenal at their disposal, they became even more formidable. But the bandits were not ones to be easily defeated."
        elif stage == 3:
            story_text = story_font.render("Stage 3: Uncharted Territories", True, (255, 255, 255))
            story_paragraph = "While traversing the vastness of space, our heroes found themselves venturing into uncharted territories. They encountered strange celestial phenomena and unexpected dangers, pushing their skills and teamwork to the limit. It was in this stage that they truly learned the value of trust and cooperation, strengthening their bond as they overcame each obstacle together."  
        elif stage == 4:
            story_text = story_font.render("Stage 4: The Betrayal", True, (255, 255, 255))
            story_paragraph = "Just when our heroes thought they were making progress, they were confronted by a betrayal within their own ranks. A crew member, once loyal, had been secretly working for the space bandits all along. In a heart-wrenching turn of events, they had to face the harsh reality that not everyone could be trusted. With heavy hearts, they pressed on, determined to see their mission through to the end."
        elif stage == 5:
            story_text = story_font.render("Stage 5: The Final Stand", True, (255, 255, 255))
            story_paragraph = "As they drew closer to the bandits' home planet, the intensity of the battles escalated. The bandits, aware of the approaching threat, deployed their most advanced ships and defenses.  The fate of the galaxy hung in the balance as they pressed forward, never losing sight of their ultimate goal."
        elif stage == 6:
            story_text = story_font.render("Stage 6: A Desperate Gamble", True, (255, 255, 255))
            story_paragraph = "In the penultimate stage, our heroes found themselves faced with a seemingly insurmountable challenge. They were outnumbered and outgunned, their ships battered and resources dwindling. In a desperate gamble, they devised a daring plan, utilizing their remaining strength to outmaneuver the bandits. The outcome of this critical stage would determine whether their mission was a success or a devastating failure."
        elif stage == 7:
            story_text = story_font.render("Stage 7: Boss Level", True, (255, 255, 255))
            story_paragraph = "This is it the moment we've all been waiting for. Our heroes reached the heart of the bandits' stronghold, facing off against the ruthless leader who had orchestrated so much chaos. In a showdown of epic proportions, they engaged in a battle of wits and skill. The odds were against them, but their determination and unwavering resolve propelled them forward. They fought with every ounce of strength, knowing that the fate of the galaxy rested on their shoulders."
        else:  # ending screen
            story_text = story_font.render("Ending Scene: Victorious Return", True, (255, 255, 255))
            story_paragraph = "Victory was hard-fought but well-deserved. Our heroes emerged triumphant, having defeated the space bandits and restored peace to the galaxy. Exhausted but filled with a sense of accomplishment, they set a course back to their home world. The galaxy hailed them as saviors, and their names would be forever etched in the annals of history. As they journeyed home, their ships glimmering against the backdrop of the cosmos, they knew that their mission was complete."
            instructions_text = instructions_font.render("Press F to go to main menu", True, (255, 255, 255))
            

        WIN.blit(story_text, story_rect)

        # Render the story paragraph with word wrapping to avoid spliting words
        paragraph_font = pygame.font.SysFont(None, 30)
        paragraph_words = story_paragraph.split()
        paragraph_lines = []
        current_line = paragraph_words[0]
        for word in paragraph_words[1:]:
            test_line = current_line + " " + word
            test_width, _ = paragraph_font.size(test_line)
            if test_width < WIDTH - 200:  # Adjust the width limit here
                current_line = test_line
            else:
                paragraph_lines.append(current_line)
                current_line = word
        paragraph_lines.append(current_line)

        paragraph_y = story_rect.bottom + 20
        for line in paragraph_lines:
            paragraph_text = paragraph_font.render(line, True, (255, 255, 255))
            paragraph_rect = paragraph_text.get_rect(center=(WIDTH // 2, paragraph_y))
            WIN.blit(paragraph_text, paragraph_rect)
            paragraph_y += 30
        WIN.blit(instructions_text, instructions_rect)


        pygame.display.update()
