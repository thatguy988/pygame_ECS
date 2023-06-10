import pygame
import sys
from systems.sound_effect_system import SoundEffectSystem


sound_system_instance = SoundEffectSystem()

sound_system_instance.add_sound_effect_component("menu_scrolling","Assets\\Sound_Effects\\Menu_Scrolling.wav")

sound_system_instance.add_sound_effect_component("press_button","Assets\\Sound_Effects\\Menu_Select_Press_2.wav")



class MenuHandling:
    def handle_menu_events(selected_option): #responsible for handling the user input events related to the main menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    sound_system_instance.play_sound_effect("menu_scrolling")
                    selected_option = (selected_option - 1) % 3  # move between 3 options
                elif event.key == pygame.K_s:
                    sound_system_instance.play_sound_effect("menu_scrolling")
                    selected_option = (selected_option + 1) % 3  
                elif event.key == pygame.K_SPACE:
                    sound_system_instance.play_sound_effect("press_button")
                    if selected_option == 0:
                        return "start_game"
                    elif selected_option == 1:
                        return "tutorial"
                    elif selected_option == 2:
                        pygame.quit()
                        sys.exit()

        return selected_option
    
    def handle_pause_menu_events(selected_option):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    sound_system_instance.play_sound_effect("menu_scrolling")
                    selected_option = (selected_option - 1) % 2  #move between 2 options
                elif event.key == pygame.K_s:
                    sound_system_instance.play_sound_effect("menu_scrolling")
                    selected_option = (selected_option + 1) % 2  
                elif event.key == pygame.K_SPACE:
                    sound_system_instance.play_sound_effect("press_button")
                    if selected_option == 0:
                        # Resume Game
                        return "resume_game"
                    elif selected_option == 1:
                        # Main Menu
                        return "main_menu"

        return selected_option
    
    
                        
                

    
                    
     