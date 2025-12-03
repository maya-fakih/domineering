import copy
from agent import Agent

class MinimaxAgent(Agent):
    def __init__(self, player_type, depth, debug=False):
        super().__init__("Minimax", player_type)
        self.depth = depth
        self.infinity = float('inf')
        self.opponent = "H" if player_type == "V" else "V"
        self.debug = debug

    def get_move(self, game):
        if self.debug:
            print(f"\n[Minimax-{self.player_type}] Starting search depth={self.depth}")
        return self.find_best_move(game, self.player_type, self.depth)

    # ---------------- MINI / MAX / MINVALUE ----------------

    def MiniMax(self, game, player, depth):
        if self.debug:
            print(f"[MM] MiniMax player={player} depth={depth}")

        if game.is_game_over() or depth == 0:
            val = game.Evaluate(self.player_type)
            if self.debug:
                print(f"[MM] Leaf depth={depth} → Eval={val}")
            return val

        if player == self.player_type:
            return self.MaxValue(game, depth)
        else:
            return self.MinValue(game, depth)

    def MaxValue(self, game, depth):
        v = -self.infinity
        moves = game.get_legal_moves(self.player_type)

        if self.debug:
            print(f"[MM] MaxValue depth={depth} | moves={len(moves)}")

        for mv in moves:
            if self.debug:
                print(f"[MM]   MAX trying {mv}")

            sim = copy.deepcopy(game)
            sim.apply_move(mv, self.player_type)

            score = self.MiniMax(sim, self.opponent, depth - 1)
            if score > v:
                v = score

            if self.debug:
                print(f"[MM]   MAX move {mv} → score={score} | best={v}")

        return v

    def MinValue(self, game, depth):
        v = self.infinity
        moves = game.get_legal_moves(self.opponent)

        if self.debug:
            print(f"[MM] MinValue depth={depth} | moves={len(moves)}")

        for mv in moves:
            if self.debug:
                print(f"[MM]   MIN trying {mv}")

            sim = copy.deepcopy(game)
            sim.apply_move(mv, self.opponent)

            score = self.MiniMax(sim, self.player_type, depth - 1)
            if score < v:
                v = score

            if self.debug:
                print(f"[MM]   MIN move {mv} → score={score} | best={v}")

        return v

    # ---------------- ROOT SEARCH ----------------

    def find_best_move(self, game, player, depth):
        best_score = -self.infinity
        best_move = None
        moves = game.get_legal_moves(player)

        if self.debug:
            print(f"[MM] Root search moves={len(moves)}")

        for mv in moves:
            if self.debug:
                print(f"[MM] ROOT trying {mv}")

            sim = copy.deepcopy(game)
            sim.apply_move(mv, player)

            score = self.MiniMax(sim, self.opponent, depth - 1)

            if score > best_score:
                best_score = score
                best_move = mv

            if self.debug:
                print(f"[MM] ROOT move {mv} → score={score} | best={best_score}")

        if self.debug:
            print(f"[MM] Selected best move: {best_move} (score={best_score})\n")

        return best_move
