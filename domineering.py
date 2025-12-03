class DomineeringGame:
    def __init__(self, size=8, depth=1, debug=False):
        self.size = size
        self.board = [["." for _ in range(size)] for _ in range(size)]
        self.turn = "V"   # V starts
        self.debug = debug

        if self.debug:
            print(f"[GAME] Initialized {size}x{size} board | depth={depth}")

    def reset(self):
        self.board = [["." for _ in range(self.size)] for _ in range(self.size)]
        self.turn = "V"

        if self.debug:
            print("[GAME] Board reset.")

    def is_valid(self, move, player):
        r1, c1, r2, c2 = move

        if not (0 <= r1 < self.size and 0 <= c1 < self.size): 
            return False
        if not (0 <= r2 < self.size and 0 <= c2 < self.size): 
            return False

        if self.board[r1][c1] != "." or self.board[r2][c2] != ".":
            return False

        if player == "V":
            return (r2 == r1 + 1 and c1 == c2)
        else:
            return (c2 == c1 + 1 and r1 == r2)

    def apply_move(self, move, player):
        r1, c1, r2, c2 = move

        if self.debug:
            print(f"[GAME] {player} plays {move}")

        if player == "H":
            self.board[r1][c1] = "H"
            self.board[r1][c2] = "h"
        else:
            self.board[r1][c1] = "V"
            self.board[r2][c1] = "v"

        self.turn = "H" if self.turn == "V" else "V"

        if self.debug:
            print(f"[GAME] Next turn: {self.turn}")

    def get_legal_moves(self, player):
        moves = []
        for r in range(self.size):
            for c in range(self.size):
                mv = (r, c, r+1, c) if player == "V" else (r, c, r, c+1)
                if self.is_valid(mv, player):
                    moves.append(mv)

        return moves

    def is_game_over(self):
        over = len(self.get_legal_moves(self.turn)) == 0
        return over

    def get_winner(self):
        if not self.is_game_over():
            return None
        loser = self.turn
        winner = "H" if loser == "V" else "V"
        return winner
    
    def Evaluate(self, player):
        if self.is_game_over():
            winner = self.get_winner()
            if winner == player:
                return 10000
            elif winner is None:
                return 0
            else:
                return -10000

        my_moves = len(self.get_legal_moves(player))
        opponent = "H" if player == "V" else "V"
        opp_moves = len(self.get_legal_moves(opponent))

        score = my_moves - opp_moves
        return score
