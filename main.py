from ui import DomineeringUI

from domineering import DomineeringGame
if __name__ == "__main__":
    ui = DomineeringUI(grid_size=15)
    ui.game = DomineeringGame(15)
    ui.current_player = "H"
    ui.run()
