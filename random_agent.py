import random
from agent import Agent

class RandomAgent(Agent):
    def __init__(self, player_type, debug=False):
        super().__init__("Random", player_type, debug=debug)

    def get_move(self, game_state):
        moves = game_state.get_legal_moves(self.player_type)

        if self.debug:
            print(f"[RANDOM] legal moves = {moves}")

        if not moves:
            if self.debug:
                print("[RANDOM] no moves available → returning None")
            return None

        mv = random.choice(moves)

        if self.debug:
            print(f"[RANDOM] selected random move = {mv}")

        return mv
