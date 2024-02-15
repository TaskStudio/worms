import math
from typing import Optional

import pygame
from pygame import Color

import src.globals as g


class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(Color(255, 0, 0))
        self.rect = self.image.get_rect(center=start_pos)
        self.start_pos = pygame.math.Vector2(start_pos)
        self.target_pos = pygame.math.Vector2(target_pos)
        self.charging_start_time = None
        self.velocity = pygame.math.Vector2(0, 0)
        self.charging = False
        self.launched = False
        self.gravity = 980  # Gravité ajustée à l'échelle du jeu (en pixels/s^2)
        self.launch_time = 0
        self.scale = 100  # 1 mètre = 100 pixels

    def calculate_initial_velocity(self, angle, speed):
        # Convertir la vitesse en pixels/s, ajustée par l'échelle
        speed_pixels = speed * self.scale
        self.velocity.x = math.cos(angle) * speed_pixels
        self.velocity.y = -math.sin(angle) * speed_pixels  # Négatif car l'axe Y est inversé dans Pygame

    def start_charging(self):
        self.charging = True
        self.charging_start_time = pygame.time.get_ticks()

    def stop_charging(self):
        if self.charging_start_time is None:
            return

        charge_duration = pygame.time.get_ticks() - self.charging_start_time
        normalized_charge = min(charge_duration / g.MAX_CHARGE_DURATION, 1)
        min_speed = 1  # m/s
        max_speed = 30  # m/s
        self.speed = min_speed + (max_speed - min_speed) * normalized_charge
        angle = math.atan2(-(self.target_pos.y - self.start_pos.y),
                           self.target_pos.x - self.start_pos.x)  # Angle ajusté
        self.calculate_initial_velocity(angle, self.speed)
        self.launch_time = pygame.time.get_ticks()
        self.charging = False
        self.launched = True

    def update(self):
        if self.launched:
            time_elapsed = (pygame.time.get_ticks() - self.launch_time) / 1000.0  # Convertir en secondes
            # Mise à jour de la position avec la formule de la physique
            displacement_x = self.velocity.x * time_elapsed
            displacement_y = self.velocity.y * time_elapsed + 0.5 * self.gravity * time_elapsed ** 2
            self.rect.x = self.start_pos.x + displacement_x
            self.rect.y = self.start_pos.y + displacement_y

    def draw_charge(self, screen, camera_position, zoom_level):
        if self.charging:
            charge_duration = pygame.time.get_ticks() - self.charging_start_time
            normalized_charge = min(charge_duration / g.MAX_CHARGE_DURATION, 1)

            charge_color = (255 * normalized_charge, 255 * (1 - normalized_charge), 0)

            # Adjust charge indicator position based on camera position and zoom
            adjusted_center = (self.rect.center - camera_position) * zoom_level
            charge_rect = pygame.Rect(
                adjusted_center[0] + 20, adjusted_center[1] - 70, 50 * zoom_level, 50 * zoom_level
            )
            pygame.draw.arc(
                screen, charge_color, charge_rect, 0, math.pi * 2 * normalized_charge, int(5 * zoom_level)
            )
