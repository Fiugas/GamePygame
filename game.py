import pygame
from player import Player
from maze import Maze
from menus import draw_start_screen, draw_pause_screen, draw_menu_screen, draw_victory_screen
from shaders.crt_shader import Shader


START, PLAYING, PAUSED, MENU, VICTORY = range(5)

class Game:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.GAME_LOGIC_SIZE, self.SCREEN_SIZE = (1500, 720), (info.current_w, info.current_h)
        self.NATIVE_SCREEN_SIZE = self.SCREEN_SIZE
        

        # Definindo as cores
        self.YELLOW = (255, 255, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Dimensões da tela
        self.WIDTH, self.HEIGHT = 1920, 1080

        # Configurações da tela
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)

        # Dimensões das células do labirinto
        self.cell_size = 50  # Tamanho das células no labirinto
        self.draw_size = 50   # Tamanho usado para desenhar o jogador e a tela

        # Cria o labirinto
        self.maze = Maze(self.WIDTH, self.HEIGHT, self.cell_size, self.draw_size)

        # Configura o relógio para controlar a taxa de quadros
        self.clock = pygame.time.Clock()

        # Estados do jogo
        self.game_state = START

        # Cria o jogador
        self.player = Player(1, 1, self.draw_size)
        self.has_key = False  # Variável para rastrear se a chave foi coletada

        # Inicializa a posição da chave
        self.key_pos = self.maze.generate_key_position()

        # Inicializa a posição da saída
        self.exit_pos = self.maze.generate_exit_position()

        # Inicializa a direção de movimento do jogador
        self.moving_direction = None

    def handle_player_movement(self, key, is_keydown):
        if key == pygame.K_w:
            self.player.direction['up'] = is_keydown
        elif key == pygame.K_s:
            self.player.direction['down'] = is_keydown
        elif key == pygame.K_a:
            self.player.direction['left'] = is_keydown
        elif key == pygame.K_d:
            self.player.direction['right'] = is_keydown

    def stop_player_movement(self, key):
        if key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
            self.moving_direction = None

    def update(self):
        if self.game_state == PLAYING:
            self.player.update(self.maze.maze)  # Passar o atributo correto do labirinto
            if (self.player.x, self.player.y) == self.key_pos:
                self.has_key = True
            if (self.player.x, self.player.y) == self.exit_pos and self.has_key:
                self.game_state = VICTORY

    def draw(self):
        if self.game_state == START:
            draw_start_screen(self.screen, self.WIDTH, self.HEIGHT)
        elif self.game_state == PLAYING:
            self.screen.fill(self.BLACK)

            # Calculate offsets
            offset_x = self.player.x * self.draw_size - self.WIDTH // 2 + self.draw_size // 2
            offset_y = self.player.y * self.draw_size - self.HEIGHT // 2 + self.draw_size // 2
            
            # Desenha o labirinto
            self.maze.draw(self.screen, offset_x, offset_y, self.WIDTH, self.HEIGHT)

            self.player.draw(self.screen, offset_x, offset_y)

            # Informações de depuração
            font = pygame.font.SysFont(None, 24)
            debug_info = [
                f"Mapa: {self.maze.width}x{self.maze.height}",
                f"Jogador: ({self.player.x}, {self.player.y})",
                f"Chave: {self.key_pos}",
                f"Saída: {self.exit_pos}"
            ]
            for i, info in enumerate(debug_info):
                text = font.render(info, True, (255, 255, 255))
                self.screen.blit(text, (10, 10 + i * 20))
            
            # Desenha o jogador
            pygame.display.update()
        elif self.game_state == PAUSED:
            draw_pause_screen(self.screen, self.WIDTH, self.HEIGHT)
        elif self.game_state == MENU:
            draw_menu_screen(self.screen, self.WIDTH, self.HEIGHT)
        elif self.game_state == VICTORY:
            draw_victory_screen(self.screen, self.WIDTH, self.HEIGHT)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if self.game_state == START:
                        self.game_state = MENU
                    elif self.game_state == PLAYING:
                        if event.key == pygame.K_p:
                            self.game_state = PAUSED
                        elif event.key == pygame.K_z:
                            self.game_state = MENU
                        elif event.key == pygame.K_0:
                            pygame.quit()
                            exit()
                        else:
                            self.handle_player_movement(event.key, True)
                    elif self.game_state == PAUSED:
                        if event.key == pygame.K_p:
                            self.game_state = PLAYING
                    elif self.game_state == MENU:
                        if event.key == pygame.K_1:
                            self.game_state = PLAYING
                        elif event.key == pygame.K_2:
                            pygame.quit()
                            exit()
                    elif self.game_state == VICTORY:
                        if event.key == pygame.K_RETURN:
                            self.game_state = START
                elif event.type == pygame.KEYUP:
                    self.handle_player_movement(event.key, False)

            self.update()
            self.draw()
            self.clock.tick(60)  # Limita a taxa de quadros a 60 FPS