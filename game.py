import pygame, os, time
from shaders.crt_shader import Shader
from states.start_screen import StartScreen

class Game:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.GAME_LOGIC_SIZE, self.SCREEN_SIZE = (1280, 720), (info.current_w, info.current_h)
        self.NATIVE_SCREEN_SIZE = self.SCREEN_SIZE
        self.game_canvas = pygame.Surface(self.GAME_LOGIC_SIZE).convert((255, 65280, 16711680, 0))
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE, pygame.FULLSCREEN | pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL)
        self.running, self.playing = True, True
        self.shader = Shader(self)
        self.player_actions = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False, 'SELECT': False, 'PAUSE': False, 'ONE': False, 'TWO': False, 'THREE': False, 'FOUR': False, 'FIVE': False}
        self.colors = {'WHITE': (255, 255, 255), 'BLACK': (0, 0, 0)}
        self.dt, self.prev_time = 0, 0
        self.state_stack = []
        self.load_assets()
        self.load_state()

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
            pygame.K_1: 'ONE',
            pygame.K_2: 'TWO',
            pygame.K_3: 'THREE',
            pygame.K_4: 'FOUR',
            pygame.K_5: 'FIVE'
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
        self.background = pygame.image.load('assets/backgrounds/background_start.png')
        self.background = pygame.transform.scale(self.background, self.SCREEN_SIZE)
        self.font = pygame.font.Font(os.path.join(self.font_dir, 'Minecrafter.Reg.ttf'), 20)

    def load_state(self):
        self.state_stack.append(StartScreen(self))

    def reset_player_actions(self):
        for action in self.player_actions:
            self.player_actions[action] = False

if __name__ == "__main__":
    game = Game()
    game.run()