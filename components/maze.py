import pygame, random
from components.entities import Key

class Maze:
    def __init__(self, level):
        self.position_type = {'OPEN': 0, 'WALL': 1}
        self.start, self.exit, self.key = None, None, None
        self.generate_maze(level)

    def generate_maze(self, level):
        self.width = 10 + (level - 1) * 5
        self.height = 10 + (level - 1) * 5
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]  # Initialize all cells as walls
        # Generate a random start position
        self.start = self.random_position('WALL')
        # Generate maze paths using DFS
        self.dfs(self.start[0], self.start[1])
        # Place key and exit after maze generation
        self.place_key_and_exit()

    def is_valid_position(self, x, y):
        # Check if a position is within maze bounds
        return 0 <= x < self.width and 0 <= y < self.height

    def is_wall(self, x, y):
        return self.grid[y][x] == self.position_type['WALL']

    def dfs(self, x, y):
        self.grid[y][x] = self.position_type['OPEN']
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid_position(nx, ny) and self.is_wall(nx, ny):
                self.grid[y + dy // 2][x + dx // 2] = self.position_type['OPEN']
                self.dfs(nx, ny)

    def place_key_and_exit(self):
        # Get all open positions
        open_positions = [
            (x, y) for y in range(self.height)
            for x in range(self.width)
            if self.grid[y][x] == self.position_type['OPEN']
            and (x, y) != self.start
        ]

        # Randomly select positions for key and exit
        key_position = random.choice(open_positions)
        self.key = Key(key_position)
        open_positions.remove(key_position)
        self.exit = random.choice(open_positions)

    def random_position(self, position_type):
        target_value = self.position_type[position_type]
        while True:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if self.grid[y][x] == target_value:
                return (x, y)

    def render(self, surface, cell_size, game):
        self.draw_maze(surface, cell_size, game)
        self.draw_borders(surface, cell_size, game)
        self.key.render(surface, cell_size, game)
        self.draw_start_and_exit(surface, cell_size, game)

    def draw_maze(self, surface, cell_size, game):
        # Draw the base maze (walls and paths)
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                if self.grid[y][x] == 1:
                    # Redimensionar e desenhar o sprite da parede
                    surface.blit(pygame.transform.scale(game.wall, (cell_size, cell_size)), rect)
                else:
                    surface.blit(pygame.transform.scale(game.path, (cell_size, cell_size)), rect)  # Light color for paths

    def draw_borders(self, surface, cell_size, game):
        # Determine which sides need borders by checking for open paths
        border_check_sides = {
            'left': any(self.grid[y][0] == 0 for y in range(self.height)),
            'right': any(self.grid[y][self.width-1] == 0 for y in range(self.height)),
            'top': any(self.grid[0][x] == 0 for x in range(self.width)),
            'bottom': any(self.grid[self.height-1][x] == 0 for x in range(self.width))
        }
        self.draw_continuous_borders(surface, cell_size, game, border_check_sides)

    def draw_continuous_borders(self, surface, cell_size, game, border_check_sides):
        # Draw continuous borders where needed
        if border_check_sides['left']:
            for y in range(self.height):
                border_rect = pygame.Rect(-cell_size, y * cell_size, cell_size, cell_size)
                pygame.draw.rect(surface, game.colors['BLACK'], border_rect)

        if border_check_sides['right']:
            for y in range(self.height):
                border_rect = pygame.Rect(self.width * cell_size, y * cell_size, cell_size, cell_size)
                pygame.draw.rect(surface, game.colors['BLACK'], border_rect)

        if border_check_sides['top']:
            for x in range(self.width):
                border_rect = pygame.Rect(x * cell_size, -cell_size, cell_size, cell_size)
                pygame.draw.rect(surface, game.colors['BLACK'], border_rect)

        if border_check_sides['bottom']:
            for x in range(self.width):
                border_rect = pygame.Rect(x * cell_size, self.height * cell_size, cell_size, cell_size)
                pygame.draw.rect(surface, game.colors['BLACK'], border_rect)

        self.fill_gaps_between_borders(surface, cell_size, game, border_check_sides)

    def fill_gaps_between_borders(self, surface, cell_size, game, border_check_sides):
        # Fill corner gaps where two borders meet
        if border_check_sides['left'] and border_check_sides['top']:
            corner_rect = pygame.Rect(-cell_size, -cell_size, cell_size, cell_size)
            pygame.draw.rect(surface, game.colors['BLACK'], corner_rect)

        if border_check_sides['left'] and border_check_sides['bottom']:
            corner_rect = pygame.Rect(-cell_size, self.height * cell_size, cell_size, cell_size)
            pygame.draw.rect(surface, game.colors['BLACK'], corner_rect)

        if border_check_sides['right'] and border_check_sides['top']:
            corner_rect = pygame.Rect(self.width * cell_size, -cell_size, cell_size, cell_size)
            pygame.draw.rect(surface, game.colors['BLACK'], corner_rect)

        if border_check_sides['right'] and border_check_sides['bottom']:
            corner_rect = pygame.Rect(self.width * cell_size, self.height * cell_size, cell_size, cell_size)
            pygame.draw.rect(surface, game.colors['BLACK'], corner_rect)

    def draw_start_and_exit(self, surface, cell_size, game):
        # Draw the start position
        start_rect = pygame.Rect(self.start[0] * cell_size, self.start[1] * cell_size, cell_size, cell_size)
        pygame.draw.rect(surface, game.colors['GREEN'], start_rect)  # Green color for the start

        # Draw the exit position
        exit_rect = pygame.Rect(self.exit[0] * cell_size, self.exit[1] * cell_size, cell_size, cell_size)
        surface.blit(pygame.transform.scale(game.exit, (cell_size, cell_size)), exit_rect)  # Blue color for the exit