import pygame
from .projectile import Projectile


class Rocket(Projectile):
    def __init__(self):
        super().__init__()
        self.rb.affected_by_wind = True
        self.image = pygame.image.load('src/assets/Sainte_roquette.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()

