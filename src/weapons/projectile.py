import math

import pygame
from pygame import Color, Surface, Vector2
from pygame.sprite import Group, Sprite

import src.globals as g
from src.physics import Rigidbody
from src.timer import Timer


class Projectile(Sprite):
    def __init__(self):
        super().__init__()
        self.rb = Rigidbody(mass=1)

        self.image = pygame.Surface((5, 5))
        self.image.fill(Color(255, 0, 0))
        self.rect = self.image.get_rect()

        self.target_pos = Vector2()

        self.charging = False
        self.launched = False

        self.launch_time = 0
        self.charge_timer = Timer()
        self.destroyed = False

    def set_position(self, position: Vector2):
        self.rb.start_pos = position
        self.rb.position = position

    def set_target(self, target: Vector2):
        self.target_pos = target

    def start_charging(self):
        self.charging = True
        self.charge_timer.start()

    def stop_charging(self):
        if self.charge_timer.get_seconds() == 0:
            return

        magnitude = self.charge_timer.get_seconds() * g.WORMS_STRENGTH
        direction = self.target_pos - self.rb.start_pos
        direction.scale_to_length(magnitude * g.m)
        self.rb.apply_forces(direction)

        self.charging = False
        self.launched = True

    def check_collision(self, worms_group: Group, *, current_worm: "Worm"):
        if self.launched:
            hit_worms = pygame.sprite.spritecollide(self, worms_group, False)
            for hit_worm in hit_worms:
                if hit_worm != current_worm:
                    hit_worm.hp = 0
                    worms_group.remove(hit_worm)
                    self.kill()
                    break

    def kill(self):
        self.destroyed = True
        super().kill()

    def update(self):
        self.rect.center = self.rb.position
        if self.charging:
            self.charge_timer.update()
        if self.launched:
            self.charge_timer.update()

            if self.rect.y > g.SCREEN_HEIGHT:
                self.launched = False
                self.kill()

    def draw(self, screen: Surface, camera_position, zoom_level):
        if self.charging:
            self._draw_charge(screen, camera_position, zoom_level)

    def _draw_charge(self, screen, camera_position, zoom_level):
        if self.charging:
            normalized_charge = min(
                self.charge_timer.get_seconds() / g.MAX_CHARGE_DURATION, 1
            )

            charge_color = (255 * normalized_charge, 255 * (1 - normalized_charge), 0)

            # Adjust charge indicator position based on camera position and zoom
            adjusted_center = (self.rect.center - camera_position) * zoom_level
            charge_rect = pygame.Rect(
                adjusted_center[0] + 20,
                adjusted_center[1] - 70,
                50 * zoom_level,
                50 * zoom_level,
            )
            pygame.draw.arc(
                screen,
                charge_color,
                charge_rect,
                0,
                math.pi * 2 * normalized_charge,
                int(5 * zoom_level),
            )
