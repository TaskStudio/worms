import math

import pygame
from pygame import Color, Surface, Vector2
from pygame.sprite import Group, Sprite

import src.globals as g
from src.timer import Timer


class Projectile(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(Color(255, 0, 0))
        self.rect = self.image.get_rect()
        self.start_pos = Vector2()
        self.target_pos = Vector2()
        self.charging_start_time = None
        self.velocity = pygame.math.Vector2(0, 0)
        self.charging = False
        self.launched = False
        self.gravity = 980  # Gravité ajustée à l'échelle du jeu (en pixels/s^2)
        self.launch_time = 0
        self.scale = 100  # 1 mètre = 100 pixels
        self.charge_timer = Timer()

    def set_position(self, position: Vector2):
        self.start_pos = position
        self.rect.center = position

    def set_target(self, target: Vector2):
        self.target_pos = target

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

    def check_collision(self, worms_group: Group, *, current_worm: "Worm"):
        if self.launched:
            hit_worms = pygame.sprite.spritecollide(self, worms_group, False)
            for hit_worm in hit_worms:
                if hit_worm != current_worm:
                    worms_group.remove(hit_worm)
                    self.kill()
                    break

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

    def draw(self, screen: Surface, camera_position, zoom_level):
        if self.charging:
            self._draw_charge(screen, camera_position, zoom_level)

    def _draw_charge(self, screen, camera_position, zoom_level):
        if self.charging:
            normalized_charge = min(
                self.charge_timer.get_seconds() / g.MAX_CHARGE_DURATION, 1)

            charge_color = (255 * normalized_charge, 255 * (1 - normalized_charge), 0)

            # Adjust charge indicator position based on camera position and zoom
            adjusted_center = (self.rect.center - camera_position) * zoom_level
            charge_rect = pygame.Rect(
                adjusted_center[0] + 20, adjusted_center[1] - 70, 50 * zoom_level, 50 * zoom_level
            )
            pygame.draw.arc(
                screen, charge_color, charge_rect, 0, math.pi * 2 * normalized_charge, int(5 * zoom_level)
            )
