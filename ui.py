import pygame
from human_agent import HumanAgent


class Button:
    def __init__(self, rect, text, callback, group=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = pygame.font.SysFont("arial", 20)
        self.group = group
        self.active = False

        self.color_idle = (210, 210, 210)
        self.color_hover = (235, 235, 235)
        self.color_active = (180, 200, 255)

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        if self.active:
            color = self.color_active
        else:
            color = self.color_hover if self.rect.collidepoint(mouse) else self.color_idle

        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        text = self.font.render(self.text, True, (0, 0, 0))
        tx = self.rect.x + (self.rect.width - text.get_width()) // 2
        ty = self.rect.y + (self.rect.height - text.get_height()) // 2
        screen.blit(text, (tx, ty))

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.group:
                for b in self.group:
                    b.active = False
            self.active = True
            self.callback(self.text)


class DomineeringUI:
    def __init__(self, grid_size=8):
        pygame.init()
        self.W, self.H = 1300, 800

        self.screen = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption("Domineering")

        self.grid_size = grid_size
        self.board_area = pygame.Rect(40, 140, 520, 520)
        self.cell = self.board_area.width // grid_size
        self.font = pygame.font.SysFont("arial", 22)

        self.board = [["." for _ in range(grid_size)] for _ in range(grid_size)]

        self.game = None
        self.current_player = None

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

    # -----------------------------
    # BUTTON CALLBACKS
    # -----------------------------
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

        self.agent_v = HumanAgent("V")
        self.agent_h = HumanAgent("H")

        self.current_player = "V"

    def on_reset(self, _):
        self.game_locked = False
        self.status_message = None
        self.turn_count = 1
        self.current_player = None
        self.hover_preview = None

        self.board = [["." for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        self.game.reset()  # IMPORTANT: Requires your Game class to implement reset()

        # clear agent pending input
        self.agent_v.pending_move = None
        self.agent_h.pending_move = None

        # allow mode selection again
        for b in self.p1_buttons + self.p2_buttons:
            b.active = False

        self.selected_p1 = None
        self.selected_p2 = None

    # -----------------------------
    # DRAWING
    # -----------------------------
    def draw_board(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.board_area, 3)

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x = self.board_area.x + c * self.cell
                y = self.board_area.y + r * self.cell

                col = (160, 160, 160) if (r + c) % 2 else (200, 200, 200)
                pygame.draw.rect(self.screen, col, (x, y, self.cell, self.cell))

                if self.board[r][c] == "V":
                    pygame.draw.rect(self.screen, (255, 80, 80), (x, y, self.cell, self.cell))
                elif self.board[r][c] == "H":
                    pygame.draw.rect(self.screen, (80, 120, 255), (x, y, self.cell, self.cell))

        if self.hover_preview:
            for (rr, cc) in self.hover_preview:
                x = self.board_area.x + cc * self.cell
                y = self.board_area.y + rr * self.cell
                pygame.draw.rect(self.screen, (0, 255, 0), (x, y, self.cell, self.cell), width=4)

    def draw_controls(self):
        t1 = self.font.render("Player 1", True, (0, 0, 0))
        t2 = self.font.render("Player 2", True, (0, 0, 0))
        self.screen.blit(t1, (930, 160))
        self.screen.blit(t2, (1130, 160))

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

    # -----------------------------
    # HELPERS
    # -----------------------------
    def pixel_to_cell(self, pos):
        x, y = pos
        col = (x - self.board_area.x) // self.cell
        row = (y - self.board_area.y) // self.cell
        return row, col

    # -----------------------------
    # MAIN TICK LOOP
    # -----------------------------
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

        # hover preview
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

        # game over
        if self.game and self.game.is_game_over():
            winner = self.game.get_winner()
            self.status_message = f"Player {winner} wins!"
            self.game_locked = False
            self.current_player = None

        # process move
        if self.game_locked and self.game and self.current_player and not self.status_message:
            agent = self.agent_v if self.current_player == "V" else self.agent_h
            move = agent.get_move(self.game)

            if move:
                self.game.apply_move(move, self.current_player)
                self.board = [row[:] for row in self.game.board]
                self.turn_count += 1
                self.current_player = self.game.turn

        # redraw
        self.screen.fill((230, 230, 230))
        self.draw_board()
        self.draw_controls()
        self.draw_stats()
        pygame.display.flip()

    def run(self):
        while True:
            self.tick()
