import copy
from agent import Agent

class ExpectimaxAgent(Agent):
    def __init__(self, player_type, depth, debug=False):
        super().__init__("Expectimax", player_type, debug=debug)
        self.depth = depth
        self.infinity = float('inf')
        self.opponent = "H" if player_type == "V" else "V"

    def get_move(self, game):
        move = self.find_best_move(game, self.player_type, self.depth)
        if self.debug:
            print(f"[DEBUG][Expectimax-{self.player_type}] best move = {move}")
        return move

    # ------------------ EXPECTIMAX CORE ------------------

    def Expectimax(self, game, player, depth):
        if game.is_game_over() or depth == 0:
            return game.Evaluate(self.player_type)

        if player == self.player_type:
            return self.MaxValue(game, depth)
        else:
            return self.ExpectedValue(game, depth)

    def MaxValue(self, game, depth):
        best = -self.infinity
        moves = game.get_legal_moves(self.player_type)

        for mv in moves:
            if self.debug:
                print(f"[DEBUG][Max] trying {mv}")

            sim = copy.deepcopy(game)
            sim.apply_move(mv, self.player_type)
            score = self.Expectimax(sim, self.opponent, depth - 1)

            if score > best:
                best = score

        return best

    def ExpectedValue(self, game, depth):
        moves = game.get_legal_moves(self.opponent)
        if not moves:
            return game.Evaluate(self.player_type)

        total = 0
        n = len(moves)

        for mv in moves:
            if self.debug:
                print(f"[DEBUG][Chance] trying {mv}")

            sim = copy.deepcopy(game)
            sim.apply_move(mv, self.opponent)
            score = self.Expectimax(sim, self.player_type, depth - 1)
            total += score

        return total / n

    # ------------------ ROOT SEARCH ------------------

    def find_best_move(self, game, player, depth):
        best_score = -self.infinity
        best_move = None

        for mv in game.get_legal_moves(player):
            if self.debug:
                print(f"[DEBUG][Root] evaluating {mv}")

            sim = copy.deepcopy(game)
            sim.apply_move(mv, player)
            score = self.Expectimax(sim, self.opponent, depth - 1)

            if score > best_score:
                best_score = score
                best_move = mv

        return best_move
