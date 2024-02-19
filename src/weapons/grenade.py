import pygame

from .projectile import Projectile


class Grenade(Projectile):
    def __init__(self):
        super().__init__()
        self.explosion_radius = 50  # Pixels
        self.image = pygame.image.load("src/assets/W4_Grenade.webp").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()

    def update(self):
        super().update()
        if self.launched:
            if self.timer.get_seconds() > 3:
                self.kill()
