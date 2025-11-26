import random
from agent import Agent

class RandomAgent(Agent):
    def __init__(self, player_type):
        super().__init__("Random", player_type)

    def get_move(self, game_state):
        moves = game_state.get_legal_moves(self.player_type)
        if not moves:
            return None
        return random.choice(moves)
