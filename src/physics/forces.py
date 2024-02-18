import random

import pygame
from pygame import Vector2


class Forces:
    @staticmethod
    def generate_wind():
        # Génère un vent aléatoire
        return Vector2(random.randint(-25, 25), random.randint(-25, 25))

    @staticmethod
    def draw_wind(screen, wind: Vector2):
        font = pygame.font.SysFont(None, 24)
        # Ajouter les coordonnées y du vent
        wind_text = f"Wind: {round(wind.magnitude())}"
        text_surface = font.render(wind_text, True, (0, 0, 0))
        screen.blit(
            text_surface, (screen.get_width() - text_surface.get_width() - 10, 10)
        )

    @staticmethod
    def draw_wind_arrow(screen, wind, origin):
        arrow_image = pygame.image.load("src/assets/arrow.png")
        arrow_image = pygame.transform.scale(arrow_image, (50, 50))
        angle = wind.angle_to(Vector2(1, 0))
        arrow_image = pygame.transform.rotate(arrow_image, angle)
        screen.blit(arrow_image, origin)
