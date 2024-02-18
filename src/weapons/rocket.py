from src.weapons import Projectile
from pygame import Vector2


class Rocket(Projectile):
    def __init__(self, wind=Vector2(0, 0)):
        super().__init__(wind=wind)

    def update(self):
        if self.launched:
            wind_effect = self.wind * 0.01
            self.rb.apply_forces(wind_effect)
        super().update()