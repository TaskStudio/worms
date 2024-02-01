import pygame
from pygame import Color


class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, speed):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(Color(255, 0, 0))
        self.rect = self.image.get_rect(center=start_pos)

        # Calculate direction vector
        self.direction = pygame.math.Vector2(target_pos) - pygame.math.Vector2(start_pos)
        self.direction = self.direction.normalize()

        self.speed = speed

    def update(self):
        self.rect.centerx += self.direction.x * self.speed
        self.rect.centery += self.direction.y * self.speed

