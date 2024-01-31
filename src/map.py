from random import randint

import pygame.draw
from pygame import Vector2


class MapElement:
    def __init__(self, *, start_x: int, start_y: int, width: int, height_diff: int, detail: int = 100) -> None:
        self.start_x: int = start_x
        self.start_y: int = start_y
        self.width: int = width
        self.height_diff: int = height_diff
        self.detail: int = detail
        self.points: list[Vector2] = []

        self.end_x: int = start_x + width

        self._generate_map()

    def _generate_map(self) -> None:
        for x in range(self.start_x, self.end_x, self.detail):
            self.points.append(Vector2(x, self.start_y-randint(0, self.height_diff)))

        self.points.append(Vector2(self.end_x, self.start_y))

        for x in range(self.end_x, self.start_x, -self.detail):
            self.points.append(Vector2(x, self.start_y))

        self.points.append(Vector2(self.start_x, self.start_y))

    def draw(self, screen) -> None:
        pygame.draw.polygon(screen, (0, 100, 0), self.points)
