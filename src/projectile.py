import pygame
from pygame import Color
import math
from typing import Optional


class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(Color(255, 0, 0))
        self.rect = self.image.get_rect(center=start_pos)
        self.target_pos = target_pos
        self.charging_start_time: Optional[float] = None
        self.direction = (pygame.math.Vector2(target_pos) - pygame.math.Vector2(start_pos)).normalize()
        self.speed = 0
        self.charging = False
        self.launched = False

    def start_charging(self):
        self.charging = True
        self.charging_start_time = pygame.time.get_ticks()

    def stop_charging(self, max_charge_duration):
        if self.charging_start_time is None:
            self.charging_start_time = pygame.time.get_ticks()

        charge_duration = pygame.time.get_ticks() - self.charging_start_time
        normalized_charge = min(charge_duration / max_charge_duration, 1)

        min_speed = 10
        max_speed = 30
        self.speed = min_speed + (max_speed - min_speed) * normalized_charge

        self.charging = False
        self.launched = True

    def update(self):
        if self.launched:
            self.rect.centerx += self.direction.x * self.speed
            self.rect.centery += self.direction.y * self.speed

    def draw_charge(self, screen, max_charge_duration):
        if self.charging:
            charge_duration = pygame.time.get_ticks() - self.charging_start_time
            normalized_charge = min(charge_duration / max_charge_duration, 1)

            charge_color = (255 * normalized_charge, 255 * (1 - normalized_charge), 0)
            charge_angle = normalized_charge * 360

            charge_rect = pygame.Rect(self.rect.centerx + 20, self.rect.centery - 70, 50, 50)
            pygame.draw.arc(screen, charge_color, charge_rect, 0, charge_angle * (math.pi / 180), 5)
