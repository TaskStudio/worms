from src.weapons import Projectile


class Rocket(Projectile):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('src/assets/Sainte_roquette.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()

