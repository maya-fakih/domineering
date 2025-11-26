from agent import Agent

class MinimaxAgent(Agent):
    def __init__(self, player_type, depth=3):
        super().__init__("Minimax", player_type)
        self.depth = depth

    def get_move(self, game_state):
        # return (r1,c1,r2,c2) or None
        best_move = None
        # minimax logic later
        return best_move
