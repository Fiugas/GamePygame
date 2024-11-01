from states.state import State

class TitleScreen(State):
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, dt, player_actions):
        if player_actions['ONE']:
            #new_state = GameWorld(self.game)
            #new_state.enter_state()
            pass
        if player_actions['TWO']:
            self.game.playing, self.game.running = False, False
        self.game.reset_player_actions()

    def render(self, surface):
        surface.blit(self.game.background, (0, 0))
        self.game.draw_text(surface, 'Menu', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 4))
        self.game.draw_text(surface, '1. Play', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3))
        self.game.draw_text(surface, '2. Quit', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3 + 20))