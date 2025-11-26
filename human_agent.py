from agent import Agent

class HumanAgent(Agent):
    def __init__(self, player_type):
        super().__init__("Human", player_type)
        self.pending_move = None

    def set_move_from_ui(self, move):
        self.pending_move = move

    def get_move(self, game):
        if self.pending_move is None:
            return None
        move = self.pending_move
        self.pending_move = None
        return move
