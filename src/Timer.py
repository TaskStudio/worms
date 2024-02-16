import pygame.font
import pygame.time
from pygame import Surface, Vector2


class Timer:
    """
    A simple timer class.

    !!! ATTENTION !!!
    This timer is not autonomous, if you want to get the time elapsed since its start correctly,
    you need to call the update method on it before getting the time. A simple solution is to call
    the update method of this class in every update methods of your classes using a Timer instance.
    """
    def __init__(self, duration: int | None = None) -> None:
        self.duration: int = duration
        self.elapsed_seconds: float = 0
        self.paused: bool = True
        self.start_tick = 0

    def start(self) -> None:
        self.paused = False
        self.start_tick = pygame.time.get_ticks()

    def reset(self) -> None:
        self.elapsed_seconds = 0.0
        self.start_tick = pygame.time.get_ticks()

    def get_countdown(self) -> int:
        return int(self.duration - self.elapsed_seconds) if self.duration else 0

    def get_seconds(self) -> float:
        return self.elapsed_seconds

    def update(self) -> None:
        if not self.paused:
            self.elapsed_seconds = (pygame.time.get_ticks() - self.start_tick) / 1000

    def draw(self, screen: Surface, position: Vector2) -> None:
        font = pygame.font.Font(None, 36)
        text = font.render(str(self.get_countdown()), True, (10, 10, 10))
        screen.blit(text, position)
