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