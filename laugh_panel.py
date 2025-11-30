import pygame
import random

class LaughPanel:
    def __init__(self):
        self.reactions = []  # list of (image, sound)
        self.current_image = None
        self.visible = False

    def load_reactions(self, count, sound_manager):
        """
        Loads reaction images + their paired sounds.
        Image: ./assets/images/reaction/laugh<i>.png
        Sound: ./assets/sounds/reaction/laugh<i>.wav
        """
        for i in range(1, count + 1):
            img = pygame.image.load(
                f"./assets/images/reaction/laugh{i}.png"
            ).convert_alpha()

            img = pygame.transform.scale(img, (150, 150))

            snd = sound_manager.load_reaction_sound(i)

            self.reactions.append((img, snd))

    def show_random(self):
        if not self.reactions:
            return
        self.current_image, sound = random.choice(self.reactions)
        sound.play()
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, screen):
        if self.visible and self.current_image:
            screen.blit(self.current_image, (600, 230))
