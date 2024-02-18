from src.weapons.projectile import Projectile


class Grenade(Projectile):
    def __init__(self):
        super().__init__()
        self.explosion_radius = 50  # Pixels
