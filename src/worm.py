import pygame
from pygame import Surface
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite


class Worm(Sprite):
    """
    Class for the worms the players will control.
    """

    def __init__(self, *, position: tuple[int, int] | Vector2 = (0, 0), scale: float = 0.2) -> None:
        super().__init__()
        original_image: Surface = pygame.image.load("src/assets/worm.png")
        scaled_size = (int(original_image.get_width() * scale), int(original_image.get_height() * scale))
        self.image: Surface = pygame.transform.scale(original_image, scaled_size)
        self.rect: Rect = self.image.get_rect(center=position)

        self.position = Vector2(position)
        self.velocity = Vector2(0, 0)
        self.speed = 0.2

        self.hp: int = 100
        self.max_hp: int = 100

    def move_right(self) -> None:
        self.velocity.x = 1

    def move_left(self) -> None:
        self.velocity.x = -1

    def stop_moving(self) -> None:
        self.velocity.x = 0

    def is_dead(self) -> bool:
        return self.hp <= 0

    def update(self, *args, **kwargs):
        self.position += self.velocity * self.speed
        self.rect.center = self.position
