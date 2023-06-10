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

    def load_stage_music(self, stage):
            music_mapping = {
                1: "game_music_1",
                2: "game_music_2",
                3: "game_music_3",
                4: "game_music_4",
                5: "game_music_5",
                6: "game_music_6",
                7: "game_music_7",
                0: "game_music_0"
            }

            if stage in music_mapping:
                music_label = music_mapping[stage]
                music_file = f"Assets\\Music\\game-music-{stage}.wav"
                self.add_music_component(music_label, music_file)
                return music_label

    def load_story_music(self, stage):
            music_mapping = {
                1: "story_music_1",
                2: "story_music_2",
                3: "story_music_3",
                4: "story_music_4",
                5: "story_music_5",
                6: "story_music_6",
                7: "story_music_7",
                8: "story_music_8"
            }

            if stage in music_mapping:
                music_label = music_mapping[stage]
                music_file = f"Assets\\Music\\story_music_{stage}.wav"
                self.add_music_component(music_label, music_file)
                return music_label