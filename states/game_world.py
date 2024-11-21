from states.state import State
from states.pause_screen import PauseScreen
from components.maze import Maze
from components.player import Player

class GameWorld(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.cell_size = 20
        self.level = 5
        self.maze = Maze(self.level)
        self.player = Player(self.maze, self.game)

    def update(self, dt, player_actions):
        self.player.update(player_actions, self.maze)
        if player_actions['PAUSE']:
            new_state = PauseScreen(self.game)
            new_state.enter_state()
        self.game.reset_player_actions()

    def render(self, dt, surface):
        surface.fill(self.game.colors['BLACK'])
        self.maze.render(surface, self.cell_size, self.game)
        self.player.render(surface, self.cell_size, self.game)