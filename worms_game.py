import pygame
from pygame import Surface, Color
from src.worm import Worm
from src.projectile import Projectile
from typing import Optional


def main() -> None:
    pygame.init()
    screen: Surface = pygame.display.set_mode((1080, 720))
    pygame.display.set_caption("WORMS")
    running: bool = True
    worm: Worm = Worm(position=(200, 200))
    worms = pygame.sprite.Group(worm)
    projectiles = pygame.sprite.Group()
    max_charge_duration: int = 3000
    current_projectile: Optional[Projectile] = None

    while running:
        screen.fill(Color(255, 243, 230))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    worm.move_left()
                elif event.key == pygame.K_RIGHT:
                    worm.move_right()
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    worm.stop_moving()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not current_projectile:
                    current_projectile = Projectile(worm.rect.center, pygame.mouse.get_pos())
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
