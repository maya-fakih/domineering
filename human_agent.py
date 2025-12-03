from agent import Agent

class HumanAgent(Agent):
    def __init__(self, player_type, debug=False):
        super().__init__("Human", player_type)
        self.pending_move = None
        self.debug = debug

    def set_move_from_ui(self, move):
        if self.debug:
            print(f"[Human-{self.player_type}] UI selected move: {move}")
        self.pending_move = move

    def get_move(self, game):
        if self.pending_move is None:
            return None

        move = self.pending_move
        self.pending_move = None

        if self.debug:
            print(f"[Human-{self.player_type}] Returning move: {move}")

        return move
