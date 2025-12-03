import pygame
from button import Button
from create_agent import create_agent
from dominos_ui import DominosUI
from sound_manager import SoundManager
from laugh_panel import LaughPanel
from text_input import TextInput

class DomineeringUI:
    def __init__(self, grid_size=8, depth=1, debug=False):
        pygame.init()
        self.W, self.H = 1300, 800
        self.depth = depth
        self.debug = debug
        input_w = 150
        input_h = 40

        p1_x = 900
        p2_x = 1100

        if self.debug:
            print("[DEBUG] DomineeringUI initialized")

        # initializing sounds
        self.sound = SoundManager()
        self.win_sound_played = False

        self.dominos = DominosUI()

        self.screen = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption("Domineering")

        self.laugh_panel = LaughPanel()
        self.laugh_panel.load_reactions(count=2, sound_manager=self.sound)

        self.title_img = pygame.image.load("./assets/images/domineering_title.png").convert_alpha()
        self.title_img = pygame.transform.scale(self.title_img, (600, 100))

        self.grid_size = grid_size
        self.board_area = pygame.Rect(40, 180, 520, 520)
        self.cell = self.board_area.width // grid_size
        self.font = pygame.font.SysFont("arial", 22)

        self.board = [["." for _ in range(grid_size)] for _ in range(grid_size)]

        self.game = None
        self.current_player = None

        # Inputs: positioned at the top with better spacing
        self.input_grid = TextInput((p1_x, 210, input_w, input_h), str(grid_size))
        self.input_depth = TextInput((p2_x, 210, input_w, input_h), str(depth))

        self.agent_h = None
        self.agent_v = None
        self.turn_count = 1
        self.hover_preview = None
        self.status_message = None

        self.selected_p1 = None
        self.selected_p2 = None
        self.game_locked = False

        modes = ["Human", "Random", "Minimax", "Minimax (α–β)", "Expectimax"]
        self.p1_buttons = []
        self.p2_buttons = []

        # Player option columns: better vertical spacing between buttons
        button_start_y = 300
        button_spacing = 55
        
        for i, m in enumerate(modes):
            b1 = Button((900, button_start_y + i * button_spacing, 150, 40), m, self.on_p1_pick)
            b2 = Button((1100, button_start_y + i * button_spacing, 150, 40), m, self.on_p2_pick)
            self.p1_buttons.append(b1)
            self.p2_buttons.append(b2)

        for b in self.p1_buttons:
            b.group = self.p1_buttons
        for b in self.p2_buttons:
            b.group = self.p2_buttons

        # Start/reset buttons with proper spacing from player buttons
        control_buttons_y = button_start_y + len(modes) * button_spacing + 30
        self.btn_start = Button((950, control_buttons_y, 250, 50), "Start Game", self.on_start)
        self.btn_reset = Button((950, control_buttons_y + 70, 250, 50), "Reset", self.on_reset)

        self.clock = pygame.time.Clock()

    # CALLBACKS ----------------------------------------------------

    def on_p1_pick(self, mode):
        if not self.game_locked:
            if self.debug:
                print(f"[DEBUG] Player 1 selected '{mode}'")
            self.selected_p1 = mode

    def on_p2_pick(self, mode):
        if not self.game_locked:
            if self.debug:
                print(f"[DEBUG] Player 2 selected '{mode}'")
            self.selected_p2 = mode

    def on_start(self, _):
        if not self.selected_p1 or not self.selected_p2:
            if self.debug:
                print("[DEBUG] Cannot start: P1 or P2 agent missing")
            return

        # -------------------------
        # READ TEXT INPUTS SAFELY
        # -------------------------
        try:
            new_grid = int(self.input_grid.text.strip())
            if new_grid < 4 or new_grid > 20:
                raise ValueError
        except:
            if self.debug:
                print("[DEBUG] Invalid grid input, using default")
            new_grid = self.grid_size

        try:
            new_depth = int(self.input_depth.text.strip())
            if new_depth < 1 or new_depth > 8:
                raise ValueError
        except:
            if self.debug:
                print("[DEBUG] Invalid depth input, using default")
            new_depth = self.depth

        # APPLY updated values
        self.grid_size = new_grid
        self.depth = new_depth
        self.cell = self.board_area.width // self.grid_size
        self.board = [["." for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        if self.debug:
            print(f"[DEBUG] Starting game — grid={self.grid_size}, depth={self.depth}")
            print(f"[DEBUG] P1:{self.selected_p1}, P2:{self.selected_p2}")

        # LOCK UI
        self.game_locked = True
        self.status_message = None
        self.turn_count = 1
        self.win_sound_played = False

        # RECREATE game (use your project module name 'domineering' which defines DomineeringGame)
        from domineering import DomineeringGame
        self.game = DomineeringGame(self.grid_size, depth=self.depth, debug=self.debug)

        # CREATE AGENTS (create_agent already accepts debug flag)
        self.agent_v = create_agent(self.selected_p1, "V", self.depth, debug=self.debug)
        self.agent_h = create_agent(self.selected_p2, "H", self.depth, debug=self.debug)

        self.current_player = "V"

    def on_reset(self, _):
        if self.debug:
            print("[DEBUG] Resetting game state")

        self.game_locked = False
        self.status_message = None
        self.turn_count = 1
        self.current_player = None
        self.hover_preview = None
        self.laugh_panel.hide()

        self.board = [["." for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        if self.game:
            if self.debug:
                print("[DEBUG] Game.reset() called")
            self.game.reset()

        # clear pending moves if agents are human
        if hasattr(self.agent_v, "pending_move"):
            self.agent_v.pending_move = None
        if hasattr(self.agent_h, "pending_move"):
            self.agent_h.pending_move = None

        for b in self.p1_buttons + self.p2_buttons:
            b.active = False

        self.btn_reset.active = False
        self.btn_start.active = False
        self.selected_p1 = None
        self.selected_p2 = None
        self.win_sound_played = False

    # DRAWING ----------------------------------------------------

    def draw_board(self):
        pygame.draw.rect(self.screen, (40, 40, 40), self.board_area, 5)
        pygame.draw.rect(self.screen, (20, 20, 20), self.board_area.inflate(-8, -8), 2)

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x = self.board_area.x + c * self.cell
                y = self.board_area.y + r * self.cell
                col = (160, 160, 160) if (r + c) % 2 else (200, 200, 200)
                pygame.draw.rect(self.screen, col, (x, y, self.cell, self.cell))

        # Domino rendering
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x = self.board_area.x + c * self.cell
                y = self.board_area.y + r * self.cell

                if self.board[r][c] == "V":
                    if r + 1 < self.grid_size:
                        self.dominos.draw_domino_V(self.screen, x, y, self.cell, self.cell, (255, 80, 80))

                elif self.board[r][c] == "H":
                    if c + 1 < self.grid_size:
                        self.dominos.draw_domino_H(self.screen, x, y, self.cell, self.cell, (80, 80, 255))

        # Hover preview (NO DEBUG PRINT)
        if self.hover_preview:
            for (rr, cc) in self.hover_preview:
                x = self.board_area.x + cc * self.cell
                y = self.board_area.y + rr * self.cell
                pygame.draw.rect(self.screen, (0, 255, 0), (x, y, self.cell, self.cell), 4)

        # Glow highlight
        if self.current_player == "V":
            glow_color = (160, 60, 60)
        elif self.current_player == "H":
            glow_color = (60, 100, 160)
        else:
            glow_color = (40, 40, 40)

        glow_surf = pygame.Surface((self.board_area.width + 20, self.board_area.height + 20), pygame.SRCALPHA)
        glow_rect = glow_surf.get_rect()
        pygame.draw.rect(glow_surf, (*glow_color, 36), glow_rect, border_radius=6)
        self.screen.blit(glow_surf, (self.board_area.x - 10, self.board_area.y - 10))

        pygame.draw.rect(self.screen, (40, 40, 40), self.board_area, 5)
        pygame.draw.rect(self.screen, (20, 20, 20), self.board_area.inflate(-8, -8), 2)

    def draw_controls(self):
        # Title at very top center (unchanged)
        self.screen.blit(self.title_img, (350, 20))

        # Labels for Grid and Depth above the text inputs
        grid_label = self.font.render("Grid", True, (0, 0, 0))
        depth_label = self.font.render("Depth", True, (0, 0, 0))
        self.screen.blit(grid_label, (900 + 50, 180))
        self.screen.blit(depth_label, (1100 + 45, 180))

        # Inputs: grid & depth placed above player option columns
        self.input_grid.draw(self.screen)
        self.input_depth.draw(self.screen)

        # Player labels positioned beneath inputs with better spacing
        t1 = self.font.render("Player 1", True, (0, 0, 0))
        t2 = self.font.render("Player 2", True, (0, 0, 0))
        self.screen.blit(t1, (900 + 25, 260))
        self.screen.blit(t2, (1100 + 25, 260))

        # Player option buttons (columns)
        for b in self.p1_buttons:
            b.draw(self.screen)
        for b in self.p2_buttons:
            b.draw(self.screen)

        # Start / Reset
        self.btn_start.draw(self.screen)
        self.btn_reset.draw(self.screen)

    def draw_stats(self):
        if self.status_message:
            t = self.font.render(self.status_message, True, (200, 0, 0))
        else:
            t = self.font.render(f"Turn: {self.turn_count}", True, (0, 0, 0))
        self.screen.blit(t, (600, 180))

    def draw_footer(self):
        text = "Made by Maya Fakih & Jana Mneimneh"
        surf = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(surf, (self.W - surf.get_width() - 20, self.H - 40))

    # UTILS -----------------------------------------------------------

    def pixel_to_cell(self, pos):
        # NO MORE DEBUG SPAM HERE
        row = (pos[1] - self.board_area.y) // self.cell
        col = (pos[0] - self.board_area.x) // self.cell
        return row, col

    # MAIN LOOP -------------------------------------------------------

    def tick(self):
        self.clock.tick(60)
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if not self.game_locked:
                for b in self.p1_buttons:
                    b.handle(event)
                for b in self.p2_buttons:
                    b.handle(event)

            self.btn_start.handle(event)
            self.btn_reset.handle(event)
            self.input_grid.handle(event)
            self.input_depth.handle(event)

            # UI clicks
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and self.game_locked
                and self.game
                and not self.status_message
            ):
                if self.board_area.collidepoint(event.pos):
                    r, c = self.pixel_to_cell(event.pos)

                    if self.current_player == "V":
                        move = (r, c, r + 1, c)
                        agent = self.agent_v
                    else:
                        move = (r, c, r, c + 1)
                        agent = self.agent_h

                    if self.debug:
                        print(f"[DEBUG] UI attempted move {move} for player {self.current_player}")

                    if self.game.is_valid(move, self.current_player):
                        if self.debug:
                            print("[DEBUG] Move VALID — passed to agent")
                        # only human agent has set_move_from_ui, safe to call for human
                        if hasattr(agent, "set_move_from_ui"):
                            agent.set_move_from_ui(move)
                    else:
                        if self.debug:
                            print("[DEBUG] Move INVALID")

        # Hover preview (no debug)
        self.hover_preview = None
        if self.game_locked and self.current_player and not self.status_message:
            if self.board_area.collidepoint(mouse):
                r, c = self.pixel_to_cell(mouse)

                if self.current_player == "V":
                    mv = (r, c, r + 1, c)
                    preview = [(r, c), (r + 1, c)]
                else:
                    mv = (r, c, r, c + 1)
                    preview = [(r, c), (r, c + 1)]

                if self.game.is_valid(mv, self.current_player):
                    self.hover_preview = preview

        # Game over (NO SPAM)
        if self.game and self.game.is_game_over():
            if not self.win_sound_played:
                if self.debug:
                    print("[DEBUG] Game over detected")
                self.sound.play("win")
                self.laugh_panel.show_random()
                self.win_sound_played = True

            winner = self.game.get_winner()

            if winner == "H":
                self.status_message = "Player 2 wins!"
            else:
                self.status_message = "Player 1 wins!"

            self.game_locked = False
            self.current_player = None

        # AGENT MOVE (KEEP DEBUG)
        if self.game_locked and self.game and self.current_player and not self.status_message:
            agent = self.agent_v if self.current_player == "V" else self.agent_h

            move = agent.get_move(self.game)

            if move:
                if self.debug:
                    print(f"[DEBUG] Agent {self.current_player} produced move {move}")

                self.game.apply_move(move, self.current_player)

                if self.current_player == "V":
                    self.sound.play("place_v")
                else:
                    self.sound.play("place_h")

                self.board = [row[:] for row in self.game.board]
                self.turn_count += 1
                self.current_player = self.game.turn

        # REDRAW
        self.screen.fill((230, 230, 230))
        self.draw_board()
        self.draw_controls()
        self.draw_stats()
        self.draw_footer()
        self.laugh_panel.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while True:
            self.tick()