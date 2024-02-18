from src.weapons import Projectile


class Rocket(Projectile):
    def __init__(self):
        super().__init__()
        self.rb.affected_by_wind = True
