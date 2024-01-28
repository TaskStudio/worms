import pygame
from pygame import Surface, Color
import math
from src.worm import Worm
from projectile import Projectile


def main() -> None:
    pygame.init()

    pygame.display.set_caption("WORMS")
    screen: Surface = pygame.display.set_mode((1080, 720))

    running: bool = True
    worm: Worm = Worm(position=(200, 200))
    worms = pygame.sprite.Group(worm)
    projectiles = pygame.sprite.Group()

    mouse_click_start_time = None
    charging = False
    max_charge_duration = 3000

    while running:
        screen.fill(color=Color(255, 243, 230))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                    case pygame.K_LEFT:
                        worm.move_left()
                    case pygame.K_RIGHT:
                        worm.move_right()

            if event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_LEFT | pygame.K_RIGHT:
                        worm.stop_moving()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click_start_time = pygame.time.get_ticks()
                charging = True

            if event.type == pygame.MOUSEBUTTONUP and charging:
                charge_duration = pygame.time.get_ticks() - mouse_click_start_time
                mouse_click_start_time = None
                charging = False

                normalized_charge = min(charge_duration / max_charge_duration, 1)
                min_speed = 1
                max_speed = 30
                projectile_speed = min_speed + (max_speed - min_speed) * (normalized_charge ** 2)

                target_pos = pygame.mouse.get_pos()
                projectile = Projectile(worm.rect.center, target_pos, projectile_speed)
                projectiles.add(projectile)

        if charging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            charge_duration = pygame.time.get_ticks() - mouse_click_start_time
            normalized_charge = min(charge_duration / max_charge_duration, 1)

            charge_color = (255 * normalized_charge, 255 * (1 - normalized_charge), 0)
            charge_angle = normalized_charge * 360

            # Position the circle slightly above the mouse cursor
            charge_rect = pygame.Rect(mouse_x + 20, mouse_y - 70, 50, 50)
            pygame.draw.arc(screen, charge_color, charge_rect, 0, charge_angle * (math.pi / 180), 5)

        worms.draw(screen)
        worms.update()
        projectiles.update()
        projectiles.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
