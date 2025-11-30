from ui import DomineeringUI

from domineering import DomineeringGame
if __name__ == "__main__":
    ui = DomineeringUI(grid_size = 10)
    ui.game = DomineeringGame(10)
    ui.current_player = "H"
    ui.run()
