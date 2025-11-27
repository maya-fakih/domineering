class DomineeringGame:
    def __init__(self, size=8):
        self.size = size
        self.board = [["." for _ in range(size)] for _ in range(size)]
        self.turn = "V"  # V starts

    def reset(self):
        self.board = [["." for _ in range(self.size)] for _ in range(self.size)]
        self.turn = "V"

    def is_valid(self, move, player):
        r1, c1, r2, c2 = move
        # inside board?
        if not (0 <= r1 < self.size and 0 <= c1 < self.size): return False
        if not (0 <= r2 < self.size and 0 <= c2 < self.size): return False

        # cells must be empty
        if self.board[r1][c1] != "." or self.board[r2][c2] != ".": return False

        # orientation
        if player == "V":
            return (r2 == r1 + 1 and c1 == c2)
        else:
            return (c2 == c1 + 1 and r1 == r2)

    def apply_move(self, move, player):
        r1, c1, r2, c2 = move

        if player == "H":
            # horizontal domino
            self.board[r1][c1] = "H"   # origin
            self.board[r1][c2] = "h"   # second half

        else:  # player == "V"
            # vertical domino
            self.board[r1][c1] = "V"   # origin
            self.board[r2][c1] = "v"   # second half

        # switch player
        self.turn = "H" if self.turn == "V" else "V"


    def get_legal_moves(self, player):
        moves = []
        for r in range(self.size):
            for c in range(self.size):
                mv = (r, c, r+1, c) if player == "V" else (r, c, r, c+1)
                if self.is_valid(mv, player):
                    moves.append(mv)
        return moves

    def is_game_over(self):
        return len(self.get_legal_moves(self.turn)) == 0

    def get_winner(self):
        if not self.is_game_over():
            return None
        # current turn player cannot move → they lose
        loser = self.turn
        winner = "H" if loser == "V" else "V"
        return winner
