import pygame
from pygame import Surface
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite


class Worm(Sprite):
    """
    Class for the worms the players will control.
    """

    def __init__(self, *, position: tuple[int, int] | Vector2 = (0, 0), scale: float = 0.2, name: str = '', player: int = 1,color=(255, 255, 255)) -> None:
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
        self.name = name
        self.player = player
        self.color = color

    def move_right(self) -> None:
        self.velocity.x = 1

    def move_left(self) -> None:
        self.velocity.x = -1

    def stop_moving(self) -> None:
        self.velocity.x = 0

    def is_dead(self) -> bool:
        return self.hp <= 0

    def draw_info(self, surface, camera_position, zoom_level):
        font = pygame.font.Font(None, int(24 * zoom_level))
        name_text = font.render(f"{self.name}", True, self.color)
        hp_text = font.render(f"HP: {self.hp}", True, self.color)

        name_text_offset_x = self.rect.width * zoom_level / 2 - name_text.get_width() / 2
        hp_text_offset_x = self.rect.width * zoom_level / 2 - hp_text.get_width() / 2

        name_text_pos = ((self.rect.topleft - camera_position) * zoom_level) - Vector2(name_text_offset_x,
                                                                                       30 * zoom_level)
        hp_text_pos = ((self.rect.topleft - camera_position) * zoom_level) - Vector2(hp_text_offset_x, 50 * zoom_level)

        surface.blit(name_text, name_text_pos)
        surface.blit(hp_text, hp_text_pos)

    def update(self, *args, **kwargs):
        self.position += self.velocity * self.speed
        self.rect.center = self.position
