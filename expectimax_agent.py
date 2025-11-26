from agent import Agent

class ExpectimaxAgent(Agent):
    def __init__(self, player_type, depth=3):
        super().__init__("Expectimax", player_type)
        self.depth = depth

    def get_move(self, game_state):
        # later
        return None
