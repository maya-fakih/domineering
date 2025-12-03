class Agent:
    def __init__(self, name, player_type, debug=False):
        self.name = name
        self.player_type = player_type
        self.debug = debug   # added

    def get_move(self, game_state):
        raise NotImplementedError
