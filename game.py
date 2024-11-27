import pygame, os, time
from shaders.crt_shader import Shader
from states.start_screen import StartScreen
from pygame import mixer


class Game:
    def __init__(self):
        pygame.init()
        mixer.init()
        info = pygame.display.Info()
        self.GAME_LOGIC_SIZE, self.SCREEN_SIZE = (1280, 720), (info.current_w, info.current_h)
        self.NATIVE_SCREEN_SIZE = self.SCREEN_SIZE
        self.game_canvas = pygame.Surface(self.GAME_LOGIC_SIZE).convert((255, 65280, 16711680, 0))
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE, pygame.FULLSCREEN | pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL)
        self.running, self.playing = True, True
        self.shader = Shader(self)
        self.player_actions = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False, 'SELECT': False, 'PAUSE': False}
        self.colors = {'WHITE': (255, 255, 255), 'BLACK': (0, 0, 0), 'GRAY': (200, 200, 200), 'BLUE': (0, 0, 255), 'GREEN': (0, 255, 0), 'RED': (255, 0, 0), 'YELLOW': (255, 255, 0)}
        self.dt, self.prev_time = 0, 0
        self.state_stack = []
        self.load_assets()
        self.load_state()
        pygame.mouse.set_visible(False)
        self.change_music()

    def run(self):
        while self.playing:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.handle_quit_event()
            if event.type == pygame.KEYDOWN:
                self.handle_key_event(event, True)
            if event.type == pygame.KEYUP:
                self.handle_key_event(event, False)

    def handle_quit_event(self):
        self.running, self.playing = False, False

    def handle_key_event(self, event, is_key_down):
        key_map = {
            pygame.K_w: 'UP',
            pygame.K_s: 'DOWN',
            pygame.K_a: 'LEFT',
            pygame.K_d: 'RIGHT',
            pygame.K_RETURN: 'SELECT',
            pygame.K_ESCAPE: 'PAUSE',
            pygame.K_UP: 'UP',
            pygame.K_DOWN: 'DOWN',
            pygame.K_LEFT: 'LEFT',
            pygame.K_RIGHT: 'RIGHT',
        }
        if event.key in key_map:
            self.player_actions[key_map[event.key]] = is_key_down

    def update(self):
        self.state_stack[-1].update(self.dt, self.player_actions)

    def render(self):
        self.state_stack[-1].render(self.dt, self.game_canvas)
        self.shader.render()
        self.screen.blit(pygame.transform.scale(self.game_canvas, self.SCREEN_SIZE), (0, 0))
        pygame.display.flip()

    def get_dt(self):
        curr_time = time.time()
        self.dt = curr_time - self.prev_time
        self.prev_time = curr_time

    def draw_text(self, surface, text, color, xy):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = xy
        surface.blit(text_surface, text_rect)

    def load_assets(self):
        self.assets_dir = os.path.join('assets')
        self.sprites_dir = os.path.join(self.assets_dir, 'sprites')
        self.font_dir = os.path.join(self.assets_dir, 'fonts')
        self.effects_dir = os.path.join(self.assets_dir, 'effects')
        self.background = pygame.image.load('assets/backgrounds/end_portal.jpg')
        self.background = pygame.transform.scale(self.background, self.SCREEN_SIZE)
        self.wall = pygame.image.load(os.path.join(self.sprites_dir, 'obsidian.jpg'))
        self.path = pygame.image.load(os.path.join(self.sprites_dir, 'end_stone.png'))
        self.player = pygame.image.load(os.path.join(self.sprites_dir, 'Dragon_Head_29.jpg'))
        self.key= pygame.image.load(os.path.join(self.sprites_dir, 'Dragon_Egg.jpg'))
        self.font = pygame.font.Font(os.path.join(self.font_dir, 'Minecrafter.Reg.ttf'), 20)
        self.player = pygame.image.load(os.path.join(self.sprites_dir, 'Dragon_Head_29.jpg'))
        self.exit = pygame.image.load('assets/backgrounds/end_portal.jpg')
        self.exit.set_alpha(200)
        self.music_tracks = [
            os.path.join(self.effects_dir, 'ko0x - Galaxy Guppy [Chiptune].mp3'),# Add more music track paths here
            os.path.join(self.effects_dir, 'Into the Maze.mp3'),
            os.path.join(self.effects_dir, 'Kubbi - Ember [Chiptune].mp3'),
            os.path.join(self.effects_dir, 'Daniel Fridell, Sven Lindvall - Trail to Dolores.mp3'),
            os.path.join(self.effects_dir, 'NEON DRIVE by Ghostrifter.mp3'),
            os.path.join(self.effects_dir, 'Ava Low - Through the Prism.mp3'),
            os.path.join(self.effects_dir, 'd4vd - Remember Me.mp3'),
            os.path.join(self.effects_dir, 'Royal & the Serpent - Wasteland.mp3'),
            os.path.join(self.effects_dir, 'Stromae, Pomme - Ma Meilleure Ennemie English.mp3'),
            os.path.join(self.effects_dir, 'To Ashes and Blood.mp3'),
        ]
        self.current_track_index = 0


    def load_state(self):
        self.state_stack.append(StartScreen(self))

    def change_music(self):
        self.current_track_index = (self.current_track_index + 1) % len(self.music_tracks)
        current_track = os.path.basename(self.music_tracks[self.current_track_index])
        mixer.music.load(self.music_tracks[self.current_track_index])
        mixer.music.play(-1)
        return current_track

    def adjust_volume(self, volume):
        # Volume should be between 0.0 and 1.0
        mixer.music.set_volume(max(0.0, min(1.0, volume)))

    def reset_player_actions(self):
        for action in self.player_actions:
            self.player_actions[action] = False

if __name__ == "__main__":
    game = Game()
    game.run()