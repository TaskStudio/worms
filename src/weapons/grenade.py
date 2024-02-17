from src.weapons.projectile import Projectile  # Assure-toi que le chemin d'importation est correct


class Grenade(Projectile):
    def __init__(self):
        super().__init__()
        self.explosion_radius = 50  # Pixels
