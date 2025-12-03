from ui import DomineeringUI

from domineering import DomineeringGame
if __name__ == "__main__":
    depth = 2
    size = 4
    debug = True
    ui = DomineeringUI(size,depth, debug = debug)
    ui.game = DomineeringGame(size, depth, debug = debug)
    ui.current_player = "H"
    ui.run()
