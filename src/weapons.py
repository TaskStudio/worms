import pygame
from src.projectile import Projectile  # Assure-toi que le chemin d'importation est correct


class Grenade(Projectile):
    def __init__(self, start_pos, target_pos):
        super().__init__(start_pos, target_pos)
        self.explosion_radius = 50  # Pixels


class Rocket(Projectile):
    def __init__(self, start_pos, target_pos, wind=(0,0)):
        super().__init__(start_pos, target_pos)
        self.wind = pygame.math.Vector2(wind)

    def update(self):
        if self.launched:
            # Applique le vent ici
            self.velocity += self.wind
            super().update()  # Continue avec la mise à jour normale


    def update(self):
        if self.launched:
            time_elapsed = (pygame.time.get_ticks() - self.launch_time) / 1000.0

            self.velocity.x += self.wind.x * time_elapsed
            self.velocity.y += self.wind.y * time_elapsed

            super().update()
