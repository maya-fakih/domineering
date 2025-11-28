from ui import DomineeringUI

from domineering import DomineeringGame
if __name__ == "__main__":
    ui = DomineeringUI(grid_size=8)
    ui.game = DomineeringGame(8)
    ui.current_player = "H"
    ui.run()
