from typing import Optional

import pygame
from pygame import Surface, Color

from src.map import MapElement
from src.projectile import Projectile
from src.worm import Worm


def main() -> None:
    pygame.init()

    screen: Surface = pygame.display.set_mode((1080, 720))
    pygame.display.set_caption("WORMS")

    worm: Worm = Worm(position=(200, 200))
    worms = pygame.sprite.Group(worm)

    projectiles = pygame.sprite.Group()
    max_charge_duration: int = 3000
    current_projectile: Optional[Projectile] = None

    map: MapElement = MapElement(start_x=0, start_y=720, width=1080, height_diff=40)

    running: bool = True
    while running:
        screen.fill(color=Color(255, 243, 230))

        map.draw(screen)
        worms.draw(screen)
        worms.update()

        # Window refresh
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                    case pygame.K_LEFT:
                        worm.move_left()
                    case pygame.K_RIGHT:
                        worm.move_right()
                    case pygame.K_r:
                        map = MapElement(
                            start_x=0, start_y=720, width=1080, height_diff=100
                        )

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    worm.stop_moving()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not current_projectile:
                    current_projectile = Projectile(
                        worm.rect.center, pygame.mouse.get_pos()
                    )
                    current_projectile.start_charging()
            if event.type == pygame.MOUSEBUTTONUP and current_projectile:
                current_projectile.stop_charging(max_charge_duration)
                projectiles.add(current_projectile)
                current_projectile = None

        worms.update()
        worms.draw(screen)

        if current_projectile and current_projectile.charging:
            current_projectile.draw_charge(screen, max_charge_duration)

        projectiles.update()
        projectiles.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
