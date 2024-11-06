from states.state import State


class Score(State):
    def __init__(self, game):
        State.__init__(self, game)


    def update(self, dt, player_actions):
        if player_actions['SELECT']:
            self.exit_state()
        self.game.reset_player_actions()

    def render(self, dt, surface):
        surface.blit(self.game.background, (0, 0))
        self.game.draw_text(surface,'Teste', self.game.colors['WHITE'], (self.game.GAME_LOGIC_SIZE[0] / 2, self.game.GAME_LOGIC_SIZE[1] / 3))