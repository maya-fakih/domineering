from agent import Agent
import copy

class AlphaBetaAgent(Agent):
    def __init__(self, player_type, depth=3):
        super().__init__("Minimax (α–β)", player_type)
        self.depth = depth
        self.infinity = float('inf')
        self.opponent = "H" if player_type == "V" else "V"

    def get_move(self, game):
        return self.find_best_move(game, self.player_type, self.depth)

    # ------------------------- MINIMAX + ALPHA-BETA -------------------------

    def MiniMax(self, game, player, depth, alpha, beta):
        if game.is_game_over() or depth == 0:
            return game.Evaluate(self.player_type)

        if player == self.player_type:
            return self.MaxValue(game, depth, alpha, beta)
        else:
            return self.MinValue(game, depth, alpha, beta)

    def MaxValue(self, game, depth, alpha, beta):
        v = -self.infinity
        moves = game.get_legal_moves(self.player_type)

        for mv in moves:
            sim = copy.deepcopy(game)
            sim.apply_move(mv, self.player_type)

            score = self.MiniMax(sim, self.opponent, depth - 1, alpha, beta)
            v = max(v, score)
            alpha = max(alpha, v)

            if alpha >= beta:    # PRUNE
                break

        return v

    def MinValue(self, game, depth, alpha, beta):
        v = self.infinity
        moves = game.get_legal_moves(self.opponent)

        for mv in moves:
            sim = copy.deepcopy(game)
            sim.apply_move(mv, self.opponent)

            score = self.MiniMax(sim, self.player_type, depth - 1, alpha, beta)
            v = min(v, score)
            beta = min(beta, v)

            if beta <= alpha:    # PRUNE
                break

        return v

    # ----------------------------- ROOT SEARCH -----------------------------

    def find_best_move(self, game, player, depth):
        alpha = -self.infinity
        beta = self.infinity
        best_score = -self.infinity
        best_move = None

        for mv in game.get_legal_moves(player):
            sim = copy.deepcopy(game)
            sim.apply_move(mv, player)

            score = self.MiniMax(sim, self.opponent, depth - 1, alpha, beta)

            if score > best_score:
                best_score = score
                best_move = mv

            alpha = max(alpha, best_score)

        return best_move
