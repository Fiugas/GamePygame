from states.state import State
from states.game_world import GameWorld
from states.resolution_screen import ResolutionScreen
from states.score_screen import Score

class TitleScreen(State):
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, dt, player_actions):
        if player_actions['ONE']:
            new_state = GameWorld(self.game)
            new_state.enter_state()
        if player_actions['TWO']:
            new_state = ResolutionScreen(self.game)
            new_state.enter_state()
        if player_actions['THREE']:
            new_state = Score(self.game)
            new_state.enter_state()
        if player_actions['FOUR']:
            self.game.playing, self.game.running = False, False
        self.game.reset_player_actions()

    def render(self, dt, surface):
        surface.blit(self.game.background, (0, 0))
        self.game.draw_text(surface, 'Menu', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 4))
        self.game.draw_text(surface, '1. Start', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 20))
        self.game.draw_text(surface, '2. Change resolution', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 40))
        self.game.draw_text(surface, '3. Score', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 60))
        self.game.draw_text(surface, '4. Exit game', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 80))