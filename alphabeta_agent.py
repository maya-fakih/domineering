from agent import Agent
import copy

class AlphaBetaAgent(Agent):
    def __init__(self, player_type, depth, debug=False):
        super().__init__("Minimax (α–β)", player_type)
        self.depth = depth
        self.infinity = float('inf')
        self.opponent = "H" if player_type == "V" else "V"
        self.debug = debug

    def get_move(self, game):
        if self.debug:
            print(f"\n[αβ-{self.player_type}] Starting search depth={self.depth}")
        return self.find_best_move(game, self.player_type, self.depth)

    # ------------------------- MINIMAX + ALPHA-BETA -------------------------

    def MiniMax(self, game, player, depth, alpha, beta):
        if self.debug:
            print(f"[αβ] MiniMax player={player} depth={depth} α={alpha} β={beta}")

        if game.is_game_over() or depth == 0:
            val = game.Evaluate(self.player_type)
            if self.debug:
                print(f"[αβ] Leaf reached depth={depth} → Eval={val}")
            return val

        if player == self.player_type:
            return self.MaxValue(game, depth, alpha, beta)
        else:
            return self.MinValue(game, depth, alpha, beta)

    def MaxValue(self, game, depth, alpha, beta):
        v = -self.infinity
        moves = game.get_legal_moves(self.player_type)

        if self.debug:
            print(f"[αβ] MaxValue depth={depth} | moves={len(moves)}")

        for mv in moves:
            if self.debug:
                print(f"[αβ]   MAX trying {mv}")

            sim = copy.deepcopy(game)
            sim.apply_move(mv, self.player_type)

            score = self.MiniMax(sim, self.opponent, depth - 1, alpha, beta)
            v = max(v, score)
            alpha = max(alpha, v)

            if self.debug:
                print(f"[αβ]   MAX move {mv} → score={score} | v={v} | α={alpha} β={beta}")

            if alpha >= beta:
                if self.debug:
                    print(f"[αβ]   PRUNE in MAX at move {mv}")
                break

        return v

    def MinValue(self, game, depth, alpha, beta):
        v = self.infinity
        moves = game.get_legal_moves(self.opponent)

        if self.debug:
            print(f"[αβ] MinValue depth={depth} | moves={len(moves)}")

        for mv in moves:
            if self.debug:
                print(f"[αβ]   MIN trying {mv}")

            sim = copy.deepcopy(game)
            sim.apply_move(mv, self.opponent)

            score = self.MiniMax(sim, self.player_type, depth - 1, alpha, beta)
            v = min(v, score)
            beta = min(beta, v)

            if self.debug:
                print(f"[αβ]   MIN move {mv} → score={score} | v={v} | α={alpha} β={beta}")

            if beta <= alpha:
                if self.debug:
                    print(f"[αβ]   PRUNE in MIN at move {mv}")
                break

        return v

    # ----------------------------- ROOT SEARCH -----------------------------

    def find_best_move(self, game, player, depth):
        alpha = -self.infinity
        beta = self.infinity
        best_score = -self.infinity
        best_move = None

        moves = game.get_legal_moves(player)
        if self.debug:
            print(f"[αβ] Root search moves={len(moves)}")

        for mv in moves:
            if self.debug:
                print(f"[αβ] ROOT trying {mv}")

            sim = copy.deepcopy(game)
            sim.apply_move(mv, player)

            score = self.MiniMax(sim, self.opponent, depth - 1, alpha, beta)

            if score > best_score:
                best_score = score
                best_move = mv

            if self.debug:
                print(f"[αβ] ROOT move {mv} → score={score} | best={best_score}")

            alpha = max(alpha, best_score)

        if self.debug:
            print(f"[αβ] Selected best move: {best_move} (score={best_score})\n")

        return best_move
