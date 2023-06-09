import pygame.mixer

from components.music_component import MusicComponent



class MusicSystem:
    def __init__(self):
        pygame.mixer.init()
        self.music_components = {}

        self.paused = {}
        self.paused_position = {}


    def add_music_component(self, label, music_file):
        component = MusicComponent(music_file)
        self.music_components[label] = component

    def get_music_component(self, label):
        return self.music_components.get(label)

    def play_music(self, label):
        component = self.get_music_component(label)
        if component and not component.playing:
            pygame.mixer.music.load(component.music_file)
            pygame.mixer.music.set_volume(component.volume)
            pygame.mixer.music.play(-1)  # Play the music indefinitely
            component.playing = True

    def pause_music(self, label):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused[label] = True
            self.paused_position[label] = pygame.mixer.music.get_pos()
    
    def resume_music(self, label):
        if self.paused[label]:
            pygame.mixer.music.unpause()
            self.paused[label] = False

    def stop_music(self, label):
        component = self.get_music_component(label)
        if component and component.playing:
            pygame.mixer.music.stop()
            component.playing = False

    def set_music_volume(self, label, volume):
        component = self.get_music_component(label)
        if component:
            component.volume = volume
            pygame.mixer.music.set_volume(component.volume)
