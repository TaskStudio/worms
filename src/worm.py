import pygame
from pygame import Surface
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite

import src.globals as g
from src.physics import Rigidbody


class Worm(Sprite):
    """
    Class for the worms the players will control.
    """

    def __init__(
        self,
        *,
        position: tuple[int, int] | Vector2 = (0, 0),
        scale: float = 0.2,
        name: str = "",
        player: int = 1,
        color=(255, 255, 255),
    ) -> None:
        Sprite.__init__(self)
        self.rb = Rigidbody(mass=g.WORMS_MASS, position=position)

        original_image: Surface = pygame.image.load("src/assets/worm.png")
        scaled_size = (
            int(original_image.get_width() * scale),
            int(original_image.get_height() * scale),
        )
        self.image: Surface = pygame.transform.scale(original_image, scaled_size)
        self.rect: Rect = self.image.get_rect(center=position)

        self.hp: int = 100
        self.max_hp: int = 100
        self.name = name
        self.player = player
        self.color = color

        self.move_force = 0.1
        self.is_moving = False

        self.weapon_fired = False

        self.arrow = pygame.image.load("src/assets/arrow.png")
        self.arrow = pygame.transform.scale(self.arrow, (30, 30))
        self.arrow = pygame.transform.rotate(self.arrow, -90)

    def move_right(self):
        if not self.is_moving:
            self.rb.set_velocity(Vector2(self.move_force, 0))
            self.is_moving = True

    def move_left(self):
        if not self.is_moving:
            self.rb.set_velocity(Vector2(-self.move_force, 0))
            self.is_moving = True

    def stop_moving(self):
        self.is_moving = False
        self.rb.clear_horizontal_velocity()

    def is_dead(self) -> bool:
        return self.hp <= 0

    def draw_info(self, surface, camera_position, zoom_level, show_arrow):
        font = pygame.font.Font(None, int(24 * zoom_level))
        name_text = font.render(f"{self.name}", True, self.color)

        # Center the name text above the worm
        name_text_pos_x = (
            self.rect.centerx - camera_position.x
        ) * zoom_level - name_text.get_width() / 2
        name_text_pos_y = (
            (self.rect.top - camera_position.y) * zoom_level
            - name_text.get_height()
            - 10 * zoom_level
        )  # Adjust the offset as needed
        name_text_pos = Vector2(name_text_pos_x, name_text_pos_y)
        surface.blit(name_text, name_text_pos)

        # Health bar dimensions and position
        hp_bar_width = 50 * zoom_level  # Width of the health bar; adjust as needed
        hp_bar_height = 5 * zoom_level  # Height of the health bar; adjust as needed

        # Center the health bar above the worm
        hp_bar_pos_x = (
            self.rect.centerx - camera_position.x
        ) * zoom_level - hp_bar_width / 2
        hp_bar_pos_y = (
            name_text_pos_y - hp_bar_height - 5 * zoom_level
        )  # Place it above the name text with a small offset
        hp_bar_position = Vector2(hp_bar_pos_x, hp_bar_pos_y)

        # Calculate health ratio
        health_ratio = max(self.hp / self.max_hp, 0)

        # Color for the health bar based on the current health ratio
        health_color = [
            int(red + (green - red) * health_ratio)
            for red, green in zip((255, 0, 0), (0, 255, 0))
        ]

        # Draw the health bar background (the "empty" part of the health bar)
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            (hp_bar_position.x, hp_bar_position.y, hp_bar_width, hp_bar_height),
        )

        # Draw the health part of the health bar
        pygame.draw.rect(
            surface,
            health_color,
            (
                hp_bar_position.x,
                hp_bar_position.y,
                hp_bar_width * health_ratio,
                hp_bar_height,
            ),
        )

        if show_arrow:
            surface.blit(
                self.arrow,
                (
                    self.rect.centerx - camera_position.x - 15,
                    self.rect.centery - camera_position.y - 125,
                ),
            )

    def update(self) -> None:
        super().update()
        self.rect.center = self.rb.position
        if self.rect.centery > g.SCREEN_HEIGHT - 50:
            self.rect.centery = g.SCREEN_HEIGHT - 50
