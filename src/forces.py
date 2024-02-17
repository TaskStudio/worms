import pygame
import random


class Forces:
    @staticmethod
    def generate_wind():
        # Génère un vent aléatoire
        return pygame.math.Vector2(random.randint(-25, 25), random.randint(-25, 25))

    @staticmethod
    def draw_wind(screen, wind):
        font = pygame.font.SysFont(None, 24)
        # Ajouter les coordonnées y du vent
        wind_text = f"Wind: {int(wind.x)} {int(wind.y)}"
        text_surface = font.render(wind_text, True, (0, 0, 0))
        screen.blit(text_surface, (screen.get_width() - text_surface.get_width() - 10, 10))

    @staticmethod
    def draw_wind_arrow(screen, wind, origin):
        scale = 1.0
        line_thickness = 5
        end_point = origin + wind * scale
        pygame.draw.line(screen, (255, 0, 0), origin, end_point, line_thickness)

        # Ajuster la taille et la position du chapeau de la flèche
        arrow_head_size = 15  # Taille plus petite pour le chapeau
        arrow_width = arrow_head_size / 2
        arrow_direction = wind.normalize()  # Direction normalisée du vent
        head_base = end_point - arrow_direction * arrow_head_size * 0.5  # Reculer légèrement la base du chapeau

        # Dessiner le chapeau de la flèche
        pygame.draw.polygon(screen, (255, 0, 0), [
            (end_point[0], end_point[1]),  # Pointe de la flèche
            (head_base[0] - arrow_width, head_base[1]),  # Côté gauche de la base du chapeau
            (head_base[0] + arrow_width, head_base[1])  # Côté droit de la base du chapeau
        ])



