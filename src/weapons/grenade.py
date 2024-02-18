import pygame

from src.weapons import Projectile


class Grenade(Projectile):
    def __init__(self):
        super().__init__()
        self.explosion_radius = 50  # Pixels
        # Load and set the grenade image
        self.image = pygame.image.load('src/assets/W4_Grenade.webp').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
