import pygame

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
