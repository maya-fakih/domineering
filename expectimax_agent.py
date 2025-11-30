from agent import Agent
import copy

class ExpectimaxAgent(Agent):
    def __init__(self, player_type, depth=3):
        super().__init__("Expectimax", player_type)
        self.depth = depth
        self.opponent = "H" if player_type == "V" else "V"
        self.infinity = float('inf')

    def get_move(self, game):
        return self.find_best_move(game, self.player_type, self.depth)

    # --------------------------------------------------------

    def ExpectiMax(self, game, player, depth):
        if game.is_game_over() or depth == 0:
            return game.Evaluate(self.player_type)

        if player == self.player_type:
            return self.MaxValue(game, depth)
        else:
            return self.ExpValue(game, depth)

    # ---------------- MAX NODE -------------------------------

    def MaxValue(self, game, depth):
        v = -self.infinity
        moves = game.get_legal_moves(self.player_type)

        for mv in moves:
            sim = copy.deepcopy(game)
            sim.apply_move(mv, self.player_type)
            score = self.ExpectiMax(sim, self.opponent, depth - 1)

            if score > v:
                v = score

        return v

    # ---------------- CHANCE NODE ----------------------------

    def ExpValue(self, game, depth):
        moves = game.get_legal_moves(self.opponent)

        if not moves:
            return game.Evaluate(self.player_type)

        p = 1 / len(moves)
        total = 0

        for mv in moves:
            sim = copy.deepcopy(game)
            sim.apply_move(mv, self.opponent)
            score = self.ExpectiMax(sim, self.player_type, depth - 1)  # FIXED
            total += p * score

        return total

    # ---------------- ROOT SEARCH ----------------------------

    def find_best_move(self, game, player, depth):
        best_score = -self.infinity
        best_move = None

        for mv in game.get_legal_moves(player):
            sim = copy.deepcopy(game)
            sim.apply_move(mv, player)
            score = self.ExpectiMax(sim, self.opponent, depth - 1)  # FIXED

            if score > best_score:
                best_score = score
                best_move = mv

        return best_move
