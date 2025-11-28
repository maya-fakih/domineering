import pygame
from button import Button
from create_agent import create_agent
from dominos_ui import DominosUI
from sound_manager import SoundManager

class DomineeringUI:
    def __init__(self, grid_size=8):
        pygame.init()
        self.W, self.H = 1300, 800

        #initializing sounds finallyyyy
        self.sound = SoundManager()
        self.win_sound_played = False
        #bringing in the dominos class making them 3d ish
        self.dominos = DominosUI()

        self.screen = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption("Domineering")

        self.title_img = pygame.image.load("./assets/images/domineering_title.png").convert_alpha()
        self.title_img = pygame.transform.scale(self.title_img, (600, 100))

        self.grid_size = grid_size
        self.board_area = pygame.Rect(40, 140, 520, 520)
        self.cell = self.board_area.width // grid_size
        self.font = pygame.font.SysFont("arial", 22)

        self.board = [["." for _ in range(grid_size)] for _ in range(grid_size)]

        self.game = None
        self.current_player = None

        self.agent_h = None
        self.agent_v = None
        self.turn_count = 1
        self.hover_preview = None
        self.status_message = None

        self.selected_p1 = None
        self.selected_p2 = None
        self.game_locked = False

        modes = ["Human", "Random", "Minimax", "Expectimax"]
        self.p1_buttons = []
        self.p2_buttons = []

        for i, m in enumerate(modes):
            b1 = Button((900, 200 + i * 50, 150, 40), m, self.on_p1_pick)
            b2 = Button((1100, 200 + i * 50, 150, 40), m, self.on_p2_pick)
            self.p1_buttons.append(b1)
            self.p2_buttons.append(b2)

        for b in self.p1_buttons:
            b.group = self.p1_buttons
        for b in self.p2_buttons:
            b.group = self.p2_buttons

        self.btn_start = Button((950, 450, 250, 50), "Start Game", self.on_start)
        self.btn_reset = Button((950, 520, 250, 50), "Reset", self.on_reset)

        self.clock = pygame.time.Clock()

    # CALLBACKS
    def on_p1_pick(self, mode):
        if not self.game_locked:
            self.selected_p1 = mode

    def on_p2_pick(self, mode):
        if not self.game_locked:
            self.selected_p2 = mode

    def on_start(self, _):
        if not self.selected_p1 or not self.selected_p2:
            return
        self.game_locked = True
        self.status_message = None
        self.turn_count = 1

        self.board = [["." for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        self.agent_v = create_agent(self.selected_p1, "V")
        self.agent_h = create_agent(self.selected_p2, "H")

        self.current_player = "V"
        self.win_sound_played = False
    
    def on_reset(self, _):
        self.game_locked = False
        self.status_message = None
        self.turn_count = 1
        self.current_player = None
        self.hover_preview = None

        self.board = [["." for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        if self.game:
            self.game.reset()

        if self.agent_v:
            self.agent_v.pending_move = None
        if self.agent_h:
            self.agent_h.pending_move = None

        for b in self.p1_buttons + self.p2_buttons:
            b.active = False

        self.btn_reset.active = False
        self.btn_start.active = False
        self.selected_p1 = None
        self.selected_p2 = None
        self.win_sound_played = False

    # DRAWING ----------------------------------------------gi---------
    def draw_board(self):
        pygame.draw.rect(self.screen, (40, 40, 40), self.board_area, 5)
        pygame.draw.rect(self.screen, (20, 20, 20), self.board_area.inflate(-8, -8), 2)

        # STEP 1 — draw all backgrounds
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x = self.board_area.x + c * self.cell
                y = self.board_area.y + r * self.cell
                col = (160, 160, 160) if (r + c) % 2 else (200, 200, 200)
                pygame.draw.rect(self.screen, col, (x, y, self.cell, self.cell))

        # STEP 2 — draw dominos ABOVE the grid
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x = self.board_area.x + c * self.cell
                y = self.board_area.y + r * self.cell

                if self.board[r][c] == "V":
                    if r+1 < self.grid_size:
                        self.dominos.draw_domino_V(self.screen, x, y, self.cell, self.cell, (255, 80, 80))

                elif self.board[r][c] == "H":
                    if c+1 < self.grid_size:
                        self.dominos.draw_domino_H(self.screen, x, y, self.cell, self.cell, (80, 80, 255))

        # Hover preview
        if self.hover_preview:
            for (rr, cc) in self.hover_preview:
                x = self.board_area.x + cc * self.cell
                y = self.board_area.y + rr * self.cell
                pygame.draw.rect(self.screen, (0, 255, 0), (x, y, self.cell, self.cell), width=4)

        # Glow overlay
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
        t1 = self.font.render("Player 1", True, (0, 0, 0))
        t2 = self.font.render("Player 2", True, (0, 0, 0))
        self.screen.blit(t1, (930, 160))
        self.screen.blit(t2, (1130, 160))

        self.screen.blit(self.title_img, (350, 20))

        for b in self.p1_buttons:
            b.draw(self.screen)
        for b in self.p2_buttons:
            b.draw(self.screen)

        self.btn_start.draw(self.screen)
        self.btn_reset.draw(self.screen)

    def draw_stats(self):
        if self.status_message:
            t = self.font.render(self.status_message, True, (200, 0, 0))
        else:
            t = self.font.render(f"Turn: {self.turn_count}", True, (0, 0, 0))
        self.screen.blit(t, (600, 180))

    # UTIL -----------------------------------------------------------
    def pixel_to_cell(self, pos):
        x, y = pos
        col = (x - self.board_area.x) // self.cell
        row = (y - self.board_area.y) // self.cell
        return row, col

    # TICK LOOP -------------------------------------------------------
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

                    if self.game.is_valid(move, self.current_player):
                        agent.set_move_from_ui(move)

        # Hover Preview ------------------------------------
        self.hover_preview = None
        if self.game_locked and self.current_player and not self.status_message:
            if self.board_area.collidepoint(mouse):
                r, c = self.pixel_to_cell(mouse)
                if self.current_player == "V":
                    move = (r, c, r + 1, c)
                    preview = [(r, c), (r + 1, c)]
                else:
                    move = (r, c, r, c + 1)
                    preview = [(r, c), (r, c + 1)]

                if self.game.is_valid(move, self.current_player):
                    self.hover_preview = preview

        # Game over ----------------------------------------
        if self.game and self.game.is_game_over():
            if not self.win_sound_played:
                self.sound.play("win")
                self.win_sound_played = True
            winner = self.game.get_winner()
            self.status_message = f"Player {winner} wins!"
            self.game_locked = False
            self.current_player = None

                
        # Agent moves --------------------------------------
        if self.game_locked and self.game and self.current_player and not self.status_message:
            agent = self.agent_v if self.current_player == "V" else self.agent_h
            move = agent.get_move(self.game)

            if move:
                self.game.apply_move(move, self.current_player)
                
                # ← ← ← PLAY SOUNDS HERE
                if self.current_player == "V":
                    self.sound.play("place_v")
                else:
                    self.sound.play("place_h")
                
                self.board = [row[:] for row in self.game.board]
                self.turn_count += 1
                self.current_player = self.game.turn

        # Redraw -------------------------------------------
        self.screen.fill((230, 230, 230))
        self.draw_board()
        self.draw_controls()
        self.draw_stats()
        pygame.display.flip()

    def run(self):
        while True:
            self.tick()
