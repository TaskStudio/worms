from src.physics import Rigidbody
from src.weapons.projectile import (
    Projectile,
)


class Grenade(Projectile):
    def __init__(self):
        super().__init__()
        Rigidbody.__init__(self, mass=1)
        self.explosion_radius = 50  # Pixels
