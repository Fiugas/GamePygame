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
        self.GAME_LOGIC_SIZE, self.SCREEN_SIZE = (1920, 1080), (info.current_w, info.current_h)
        self.NATIVE_SCREEN_SIZE = self.SCREEN_SIZE


        # Definindo as cores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)    # Cor da saída

        # Configurações da tela
        self.screen = pygame.display.set_mode((self.SCREEN_SIZE[0],self.SCREEN_SIZE[1]), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)

        # Dimensões das células do labirinto
        self.cell_size = 50  # Tamanho das células no labirinto
        self.draw_size = 100   # Tamanho usado para desenhar o jogador e a tela

        # chave
        try:
            self.key_sprite = pygame.image.load('sprites/Dragon_Egg.jpg')
            # Redimensiona o sprite para o tamanho da célula
            self.key_sprite = pygame.transform.scale(self.key_sprite, (self.draw_size, self.draw_size))
        except pygame.error:
            print("Não foi possível carregar a imagem da chave. Usando retângulo como fallback.")
            self.key_sprite = None


        # Nível do jogo
        self.level = 1  # Começa no nível 1

        # Cria o labirinto
        self.maze = Maze(self.level, self.cell_size, self.draw_size)

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


    def restart_game(self):
        """Reinicia o jogo com o próximo nível."""
        self.level += 1
        self.maze = Maze(self.level, self.cell_size, self.draw_size)
        self.player = Player(1, 1, self.draw_size)
        self.has_key = False
        self.key_pos = self.maze.generate_key_position()
        self.exit_pos = self.maze.generate_exit_position()
        self.game_state = PLAYING

    def update(self):
        if self.game_state == PLAYING:
            self.player.update(self.maze.maze)  # Passar o atributo correto do labirinto
            if (self.player.x, self.player.y) == self.key_pos:
                self.has_key = True
            if (self.player.x, self.player.y) == self.exit_pos and self.has_key:
                self.restart_game()  # Reinicia o jogo com o próximo nível

    def calculate_offset(self):
        offset_x = self.player.x * self.draw_size - self.SCREEN_SIZE[0] // 2 + self.draw_size // 2
        offset_y = self.player.y * self.draw_size - self.SCREEN_SIZE[1] // 2 + self.draw_size // 2
        return offset_x, offset_y

    def draw_key(self, offset_x, offset_y):
        key_draw_x = self.key_pos[0] * self.draw_size - offset_x
        key_draw_y = self.key_pos[1] * self.draw_size - offset_y
        self.screen.blit(self.key_sprite, (key_draw_x, key_draw_y))

    def draw_exit(self, offset_x, offset_y):
        exit_draw_x = self.exit_pos[0] * self.draw_size - offset_x
        exit_draw_y = self.exit_pos[1] * self.draw_size - offset_y
        pygame.draw.rect(self.screen, self.BLUE, (exit_draw_x, exit_draw_y, self.draw_size, self.draw_size))

    def draw_info(self):
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

    def draw(self):
        if self.game_state == START:
            draw_start_screen(self.screen, self.SCREEN_SIZE[0], self.SCREEN_SIZE[1])
        elif self.game_state == PLAYING:
            self.screen.fill(self.BLACK)

            # Calculate offsets
            offset_x, offset_y = self.calculate_offset()

            # Desenha o labirinto
            self.maze.draw(self.screen, offset_x, offset_y, self.SCREEN_SIZE[0], self.SCREEN_SIZE[1])

            self.player.draw(self.screen, offset_x, offset_y)

            if self.has_key is not True:
                # Desenha a chave
                self.draw_key(offset_x, offset_y)

            # Desenha a saída
            self.draw_exit(offset_x, offset_y)

            # Informações de depuração
            self.draw_info()

            # Desenha o jogador
            pygame.display.update()
        elif self.game_state == PAUSED:
            draw_pause_screen(self.screen, self.SCREEN_SIZE[0], self.SCREEN_SIZE[1])
        elif self.game_state == MENU:
            draw_menu_screen(self.screen, self.SCREEN_SIZE[0], self.SCREEN_SIZE[1])
        elif self.game_state == VICTORY:
            draw_victory_screen(self.screen, self.SCREEN_SIZE[0], self.SCREEN_SIZE[1])


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
                        if event.key == pygame.K_ESCAPE:
                            self.game_state = PAUSED
                        else:
                            self.handle_player_movement(event.key, True)
                    elif self.game_state == PAUSED:
                        if event.key == pygame.K_ESCAPE:
                            self.game_state = PLAYING
                        elif event.key == pygame.K_z:
                            self.game_state = MENU
                        elif event.key == pygame.K_0:
                            pygame.quit()
                            exit()
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