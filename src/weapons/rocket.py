import pygame

from src.weapons import Projectile


class Rocket(Projectile):
    def __init__(self, wind=(0,0)):
        super().__init__()
        self.wind = pygame.math.Vector2(wind)

    def update(self):
        super().update()
        if self.launched:
            time_elapsed = (pygame.time.get_ticks() - self.launch_time) / 1000.0

            self.velocity.x += self.wind.x * time_elapsed
            self.velocity.y += self.wind.y * time_elapsed
