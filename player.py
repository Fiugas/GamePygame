import pygame

class Player:
    def __init__(self, x, y, draw_size):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.draw_size = draw_size
        self.speed = 1  # Velocidade do jogador
        self.direction = {'up': False, 'down': False, 'left': False, 'right': False}
        self.frame_count = 0
        self.move_interval = 5  # Intervalo de movimento em quadros

    def move(self, direction, maze):
        if direction == 'up' and self.can_move(self.x, self.y - 1, maze):
            self.y -= self.speed
        elif direction == 'down' and self.can_move(self.x, self.y + 1, maze):
            self.y += self.speed
        elif direction == 'left' and self.can_move(self.x - 1, self.y, maze):
            self.x -= self.speed
        elif direction == 'right' and self.can_move(self.x + 1, self.y, maze):
            self.x += self.speed

    def can_move(self, x, y, maze):
        # Verifica se o jogador pode se mover para a posição (x, y)
        return maze[y, x] == 0

    def update(self, maze):
        self.frame_count += 1
        if self.frame_count >= self.move_interval:
            if self.direction['up']:
                self.move('up', maze)
            if self.direction['down']:
                self.move('down', maze)
            if self.direction['left']:
                self.move('left', maze)
            if self.direction['right']:
                self.move('right', maze)
            self.frame_count = 0  # Reinicia o contador de quadros

    def draw(self, surface, offset_x, offset_y):
        draw_x = self.x * self.draw_size - offset_x
        draw_y = self.y * self.draw_size - offset_y
        try:
            self.player_sprite = pygame.image.load('sprites/Dragon_Head_29.jpg')
            # Redimensiona o sprite para o tamanho da célula
            self.player_sprite = pygame.transform.scale(self.player_sprite, (self.draw_size, self.draw_size))
        except pygame.error:
            print("Não foi possível carregar a imagem da chave. Usando retângulo como fallback.")
            self.player_sprite = None
        surface.blit(self.player_sprite, (draw_x, draw_y))