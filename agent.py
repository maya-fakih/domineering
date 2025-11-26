class Agent:
    def __init__(self, name, player_type):
        self.name = name
        self.player_type = player_type #can be vertical or horizontal
        
    def get_move(self, game_state):
        raise NotImplementedError
    
#note to self:
#     player can be
#     "Human"
#     "Random AI"
#     "Minimax"
#     "Expectimax"
#     "SuperHardAI"

