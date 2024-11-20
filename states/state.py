class State():
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def blink_message(self, dt):
        self.blink_timer_seconds -= dt
        if self.blink_timer_seconds < 0:
            self.is_text_hidden = not self.is_text_hidden
            self.set_blink_timer()

    def set_blink_timer(self):
        self.blink_timer_seconds = 0.75

    def update_cursor(self, keys):
        if keys['UP']:
            self.handle_arrow_up_key()
        if keys['DOWN']:
            self.handle_arrow_down_key()

    def handle_arrow_up_key(self):
        self.menu_cursor = (self.menu_cursor - 1) % len(self.menu_options)

    def handle_arrow_down_key(self):
        self.menu_cursor = (self.menu_cursor + 1) % len(self.menu_options)

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()