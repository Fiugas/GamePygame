import pygame
from player import Player
from maze import Maze
from assets import draw_start_screen, draw_pause_screen, draw_menu_screen, draw_victory_screen
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
        self.WIDTH, self.HEIGHT = 1500, 720

        # Configurações da tela
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # Dimensões das células do labirinto
        self.cell_size = 45  # Tamanho das células no labirinto
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

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # Limita a taxa de quadros a 60 FPS

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                    if self.game_state == START:
                        self.game_state = MENU
                    elif self.game_state == MENU:
                        if event.key == pygame.K_1:
                            print("Iniciar jogo")
                            self.game_state = PLAYING
                        elif event.key == pygame.K_2:
                            run = False
                    elif self.game_state == PLAYING:
                        if event.key == pygame.K_p:
                            self.game_state = PAUSED
                        else:
                            self.handle_player_movement(event.key)
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

    def handle_player_movement(self, key):
        if key == pygame.K_w:
            self.player.move('up', self.maze.maze)
        elif key == pygame.K_s:
            self.player.move('down', self.maze.maze)
        elif key == pygame.K_a:
            self.player.move('left', self.maze.maze)
        elif key == pygame.K_d:
            self.player.move('right', self.maze.maze)

    def update(self):
        if self.game_state == PLAYING:
            self.player.update()
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
            
            # Desenha o jogador
            self.player.draw(self.screen, offset_x, offset_y)
            pygame.display.update()
        elif self.game_state == PAUSED:
            draw_pause_screen(self.screen, self.WIDTH, self.HEIGHT)
        elif self.game_state == MENU:
            draw_menu_screen(self.screen, self.WIDTH, self.HEIGHT)
        elif self.game_state == VICTORY:
            draw_victory_screen(self.screen, self.WIDTH, self.HEIGHT)

    def show_victory_screen(self):
        """ Mostra a tela de vitória."""
        self.screen.fill(self.BLACK)
        font = pygame.font.Font(None, 74)
        text = font.render("Você venceu!", True, self.WHITE)
        self.screen.blit(text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)