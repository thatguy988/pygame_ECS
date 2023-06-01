import pygame
import os


class RenderSystem:
    @staticmethod
    def render(entity, surface):
        if entity.alive:
            if hasattr(entity, 'image'):
                surface.blit(entity.image, (entity.position.x, entity.position.y))
   


    def update_health_text(current_time, yellow, red, prev_yellow_health, prev_red_health, font,
                       last_yellow_health_change,last_red_health_change,yellow_health_text,red_health_text,player_count):#move to render system file
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