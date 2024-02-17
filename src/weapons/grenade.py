import pygame
from src.weapons.projectile import Projectile  # Assure-toi que le chemin d'importation est correct


class Grenade(Projectile):
    def __init__(self):
        super().__init__()
        self.explosion_radius = 50  # Pixels

    def update(self):
        if self.launched:
            # Applique le vent ici
            self.velocity += self.wind
            super().update()  # Continue avec la mise à jour normale
