import pygame
from pygame import Surface
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite


class Worm(Sprite):
    """
    Class for the worms the players will control.
    """

    def __init__(self, *, position: tuple[int, int] | Vector2 = (0, 0)) -> None:
        # Setup for the sprite class
        super().__init__()
        self.image: Surface = pygame.image.load("src/assets/worm.png")
        self.rect: Rect = self.image.get_rect(center=position)

        self.position: Vector2 = Vector2(position)
        self.velocity: Vector2 = Vector2(0, 0)
        self.speed: float = 0.5

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

    def update(self) -> None:
        self.position += self.velocity * self.speed
        self.rect.center = self.position
