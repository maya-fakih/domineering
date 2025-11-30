import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        # normal game sounds
        self.sounds = {
            "place_v": pygame.mixer.Sound("assets/sounds/place_v.wav"),
            "place_h": pygame.mixer.Sound("assets/sounds/place_h.wav"),
            "win": pygame.mixer.Sound("assets/sounds/win.wav"),
        }

    def load_reaction_sound(self, i):
        """Used by LaughPanel to load laugh<i>.wav"""
        return pygame.mixer.Sound(f"./assets/sounds/reaction/laugh{i}.wav")

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()
