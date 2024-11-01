from states.state import State
from states.game_world import GameWorld
from states.resolution_screen import ResolutionScreen

class TitleScreen(State):
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, dt, player_actions):
        if player_actions['ONE']:
            new_state = GameWorld(self.game)
            new_state.enter_state()
            pass
        if player_actions['TWO']:
            new_state = ResolutionScreen(self.game)
            new_state.enter_state()
        if player_actions['THREE']:
            self.game.playing, self.game.running = False, False
        self.game.reset_player_actions()

    def render(self, surface):
        surface.fill(self.game.colors['BLACK'])
        self.game.draw_text(surface, 'Menu', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 4))
        self.game.draw_text(surface, '1. Start', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3))
        self.game.draw_text(surface, '2. Change resolution', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 20))
        self.game.draw_text(surface, '3. Exit', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 40))