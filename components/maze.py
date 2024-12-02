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

    def render(self, surface, cell_size, game, visibility_check=None, player = None, camera=None):
        self.draw_maze(surface, cell_size, visibility_check, player, game, camera)
        self.key.render(surface, cell_size, game, camera, visibility_check, player)
        # Render key and exit with camera transformation
        self.draw_start_and_exit(surface, cell_size, game, camera, visibility_check, player)

    def draw_maze(self, surface, cell_size, visibility_check,  player, game, camera):
        # Draw the base maze (walls and paths)
        for y in range(self.height):
            for x in range(self.width):
                screen_x = x * cell_size
                screen_y = y * cell_size
                if camera:
                    screen_x, screen_y = camera.apply(x, y)
                if visibility_check and not visibility_check(x, y, player):
                    continue
                if self.grid[y][x] == 1:
                    surface.blit(pygame.transform.scale(game.wall, (cell_size, cell_size)), (screen_x, screen_y))
                else:
                    surface.blit(pygame.transform.scale(game.path, (cell_size, cell_size)), (screen_x, screen_y))  # Light color for paths

    def draw_start_and_exit(self, surface, cell_size, game, camera, visibility_check, player):
        # Render key and exit with camera transformation
        if camera:
            Start_screen_x, Start_screen_y = camera.apply(self.start[0], self.start[1])
            exit_screen_x, exit_screen_y = camera.apply(self.exit[0], self.exit[1])
        else:
            Start_screen_x = self.start[0] * cell_size
            Start_screen_y = self.start[1] * cell_size
            exit_screen_x = self.exit[0] * cell_size
            exit_screen_y = self.exit[1] * cell_size

        if visibility_check is None or visibility_check(self.exit[0], self.exit[1], player):
            surface.blit(pygame.transform.scale(game.exit, (cell_size, cell_size)), (exit_screen_x, exit_screen_y))
        if visibility_check is None or visibility_check(self.start[0], self.start[1], player):
            pygame.draw.rect(surface, game.colors['GREEN'], pygame.Rect(Start_screen_x, Start_screen_y, cell_size, cell_size))  # Green color for the start
