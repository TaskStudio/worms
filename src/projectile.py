import math

import pygame
from pygame import Color

import src.globals as g
from src.Timer import Timer


class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(Color(255, 0, 0))
        self.rect = self.image.get_rect(center=start_pos)
        self.start_pos = pygame.math.Vector2(start_pos)
        self.target_pos = pygame.math.Vector2(target_pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self.charging = False
        self.launched = False
        self.gravity = 980  # Gravité ajustée à l'échelle du jeu (en pixels/s^2)
        self.launch_time = 0
        self.scale = 100  # 1 mètre = 100 pixels
        self.charge_timer = Timer()

    def calculate_initial_velocity(self, angle, speed):
        # Convertir la vitesse en pixels/s, ajustée par l'échelle
        speed_pixels = speed * self.scale
        self.velocity.x = math.cos(angle) * speed_pixels
        self.velocity.y = (
            -math.sin(angle) * speed_pixels
        )  # Négatif car l'axe Y est inversé dans Pygame

    def start_charging(self):
        self.charging = True
        self.charge_timer.start()

    def stop_charging(self):
        if self.charge_timer.get_seconds() == 0:
            return

        normalized_charge = min(
            self.charge_timer.get_seconds() / g.MAX_CHARGE_DURATION, 1
        )
        min_speed = 1  # m/s
        max_speed = 30  # m/s
        self.speed = min_speed + (max_speed - min_speed) * normalized_charge
        angle = math.atan2(
            -(self.target_pos.y - self.start_pos.y),
            self.target_pos.x - self.start_pos.x,
        )  # Angle ajusté
        self.calculate_initial_velocity(angle, self.speed)
        self.launch_time = self.charge_timer.get_seconds()
        self.charging = False
        self.launched = True

    def update(self):
        if self.charging:
            self.charge_timer.update()
        if self.launched:
            self.charge_timer.update()
            time_elapsed = (
                self.charge_timer.get_seconds() - self.launch_time
            )  # Convertir en secondes
            # Mise à jour de la position avec la formule de la physique
            displacement_x = self.velocity.x * time_elapsed
            displacement_y = (
                self.velocity.y * time_elapsed + 0.5 * self.gravity * time_elapsed**2
            )
            self.rect.x = self.start_pos.x + displacement_x
            self.rect.y = self.start_pos.y + displacement_y

    def draw_charge(self, screen):
        if self.charging:
            normalized_charge = min(
                self.charge_timer.get_seconds() / g.MAX_CHARGE_DURATION, 1
            )

            charge_color = (255 * normalized_charge, 255 * (1 - normalized_charge), 0)
            charge_angle = normalized_charge * 360

            charge_rect = pygame.Rect(
                self.rect.centerx + 20, self.rect.centery - 70, 50, 50
            )
            pygame.draw.arc(
                screen, charge_color, charge_rect, 0, charge_angle * (math.pi / 180), 5
            )
