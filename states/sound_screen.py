import pygame
import os
from states.state import State

class ConfigureSound(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.menu_options = {0: 'Volume', 1: 'Change Music', 2: 'Back'}
        self.menu_cursor = 0
        self.volume = 0.5  # Default volume at 50%
        self.is_music_paused = False
        self.current_music = os.path.basename(self.game.music_tracks[self.game.current_track_index])
    
    def update(self, dt, player_actions):
        self.update_cursor(player_actions)
        
        if self.menu_cursor == 0:
            if player_actions['LEFT']:
                self.volume = max(0.0, self.volume - 0.1)
                self.game.adjust_volume(self.volume)
            if player_actions['RIGHT']:
                self.volume = min(1.0, self.volume + 0.1)
                self.game.adjust_volume(self.volume)
        if self.menu_cursor == 1:
            if player_actions['LEFT']:
                self.change_music_track(-1)
            elif player_actions['RIGHT']:
                self.change_music_track(1)
        if player_actions['SELECT']:
                self.toggle_music_pause()
        if player_actions['SELECT']:
            selected_option = self.menu_options[self.menu_cursor]
            self.handle_selected_option(selected_option)
        self.game.reset_player_actions()

    def change_music_track(self, direction):
        self.current_music = self.game.change_music() if direction > 0 else self.get_previous_track()

    def get_previous_track(self):
        prev_index = (self.game.current_track_index - 1 + len(self.game.music_tracks)) % len(self.game.music_tracks)
        self.game.current_track_index = prev_index
        current_track = os.path.basename(self.game.music_tracks[prev_index])
        pygame.mixer.music.load(self.game.music_tracks[prev_index])
        pygame.mixer.music.play(-1)
        return current_track

    def toggle_music_pause(self):
        if pygame.mixer.music.get_busy():
            if self.is_music_paused:
                pygame.mixer.music.unpause()
                self.is_music_paused = False
            else:
                pygame.mixer.music.pause()
                self.is_music_paused = True

    def handle_selected_option(self, option):
        if option == 'Change Music':
            self.current_music = self.game.change_music()
        if option == 'Back':
            self.exit_state()
        self.game.reset_player_actions()

    def render(self, dt, surface):
        surface.blit(self.game.background, (0, 0))
        self.game.draw_text(surface, 'Configure Sound', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 4))
        volume_text = f'Volume: {int(self.volume * 100)}%'
        self.game.draw_text(surface, volume_text, self.game.colors['WHITE'] if self.menu_cursor == 0 else self.game.colors['GRAY'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3))
        music_status = 'Paused' if self.is_music_paused else 'Playing'
        current_music_text = f'Current Music: {self.current_music} ({music_status})'
        self.game.draw_text(surface, current_music_text, self.game.colors['WHITE'] if self.menu_cursor == 1 else self.game.colors['GRAY'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 20))
        self.game.draw_text(surface, 'Back', self.game.colors['WHITE'] if self.menu_cursor == 2 else self.game.colors['GRAY'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 40))