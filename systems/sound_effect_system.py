import pygame
from components.sound_effect_component import SoundEffectComponent
class SoundEffectSystem:
    def __init__(self):
        pygame.mixer.init()
        self.sound_components = {}

    def add_sound_effect_component(self, label, sound_file):
        component = SoundEffectComponent(sound_file)
        self.sound_components[label] = component

    def get_sound_effect_component(self, label):
        return self.sound_components.get(label)

    def play_sound_effect(self, label):
        component = self.get_sound_effect_component(label)
        if component:
            sound = pygame.mixer.Sound(component.sound_file)
            sound.set_volume(component.volume)
            sound.play()

    def set_sound_effect_volume(self, label, volume):
        component = self.get_sound_effect_component(label)
        if component:
            component.volume = volume
            
    def stop_sound_effect(self, label):
        component = self.get_sound_effect_component(label)
        if component:
            pygame.mixer.find_channel().stop()

    def stop_all_sound_effects(self):
        pygame.mixer.stop()

    def load_sound_effects(self):
        self.add_sound_effect_component("menu_scrolling","Assets\\Sound_Effects\\Menu_Scrolling.wav")
        self.add_sound_effect_component("press_button","Assets\\Sound_Effects\\Menu_Select_Press_2.wav")
        self.add_sound_effect_component("menu_scrolling","Assets\\Sound_Effects\\Menu_Scrolling.wav")
        self.add_sound_effect_component("press_button","Assets\\Sound_Effects\\Menu_Select_Press_2.wav")
        self.add_sound_effect_component("game_over","Assets\\Sound_Effects\\Game_Over_Sound.wav")
        self.add_sound_effect_component("start_up_1","Assets\\Sound_Effects\\sega-scream.mp3")
        self.add_sound_effect_component("start_up_2","Assets\\Sound_Effects\\sega-saturn-startup.mp3")
        self.add_sound_effect_component("bulletshot","Assets\\Sound_Effects\\Bullet_Shoot.wav")
        self.add_sound_effect_component("enemyshot","Assets\\Sound_Effects\\Enemy_Bullet.wav")
        self.add_sound_effect_component("playerhit","Assets\\Sound_Effects\\Bullet_Hit_With_Player.wav")
        self.add_sound_effect_component("enemyhit","Assets\\Sound_Effects\\Bullet_Hit_With_Enemy.wav")
        self.add_sound_effect_component("playerdeath","Assets\\Sound_Effects\\Player_Ship_Destroyed.wav")
        self.add_sound_effect_component("score","Assets\\Sound_Effects\\Add_Score_Sound.wav")
        self.add_sound_effect_component("explosion","Assets\\Sound_Effects\\Explosion_Sound.wav")


