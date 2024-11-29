from states.state import State
from states.pause_screen import PauseScreen
from states.nextlevel_screen import Nextlevelscreen
from components.maze import Maze
from components.player import Player
from components.camera import Camera


class GameWorld(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.cell_size = 20
        self.level = 1
        self.maze = Maze(self.level)
        self.maze.cell_size = self.cell_size 
        self.player = Player(self.maze, self.game)
        self.camera = Camera(self.maze)


    def update(self, dt, player_actions):
        self.player.update(player_actions, self.maze)
        self.camera.update(self.player.x, self.player.y)
        if player_actions['PAUSE']:
            new_state = PauseScreen(self.game)
            new_state.enter_state()
        if self.maze.key.collected and self.player.collision.check_exit_collision(self.player.x, self.player.y):
            new_state = Nextlevelscreen(self.game)
            self.level += 2
            self.maze.generate_maze(self.level)
            self.player.update_maze(self.maze)
            self.camera.update_maze(self.maze)
            new_state.enter_state()
        self.game.reset_player_actions()

    def render(self, dt, surface):
        surface.fill(self.game.colors['BLACK'])
        self.maze.render(surface, self.cell_size, self.game, 
                    visibility_check=self.camera.is_in_view_range, 
                    player= self.player,
                    camera=self.camera)
        self.player.render(surface, self.cell_size, self.game, camera=self.camera)
        self.camera.apply_fog(surface, self.player.x, self.player.y)