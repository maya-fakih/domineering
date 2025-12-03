import pygame

class TextInput:
    def __init__(self, rect, placeholder="", max_len=3):
        self.rect = pygame.Rect(rect)
        self.placeholder = placeholder
        self.max_len = max_len
        self.text = ""
        self.active = False
        self.font = pygame.font.SysFont("arial", 22)
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if not self.active:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.active = False  # Deactivate on Enter
            else:
                if len(self.text) < self.max_len and event.unicode.isdigit():
                    self.text += event.unicode

    def draw(self, screen):
        # Change border color and thickness when active
        if self.active:
            border_color = (50, 150, 255)  # Blue when active
            border_width = 3
            bg_color = (245, 250, 255)  # Light blue tint
        else:
            border_color = (100, 100, 100)  # Gray when inactive
            border_width = 2
            bg_color = (255, 255, 255)  # White
        
        # Draw background
        pygame.draw.rect(screen, bg_color, self.rect)
        # Draw border
        pygame.draw.rect(screen, border_color, self.rect, border_width)

        # Render text or placeholder
        if self.text:
            surf = self.font.render(self.text, True, (0, 0, 0))
        else:
            surf = self.font.render(self.placeholder, True, (150, 150, 150))

        screen.blit(surf, (self.rect.x + 8, self.rect.y + 8))

        # Draw blinking cursor when active
        if self.active:
            self.cursor_timer += 1
            if self.cursor_timer > 30:  # Blink every 30 frames
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
            
            if self.cursor_visible:
                text_width = surf.get_width() if self.text else 0
                cursor_x = self.rect.x + 8 + text_width
                cursor_y = self.rect.y + 8
                pygame.draw.line(screen, (0, 0, 0), 
                               (cursor_x, cursor_y), 
                               (cursor_x, cursor_y + 24), 2)

    def get_value(self):
        return self.text.strip()