import pygame
from pygame import Surface, Color
from src.worm import Worm
from projectile import Projectile  # Import the Projectile class


def main() -> None:
    pygame.init()

    pygame.display.set_caption("WORMS")
    screen: Surface = pygame.display.set_mode((1080, 720))

    running: bool = True
    worm: Worm = Worm(position=(200, 200))
    worms = pygame.sprite.Group(worm)
    projectiles = pygame.sprite.Group()  # Group for projectiles

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
                # Create a projectile when the mouse is clicked
                target_pos = pygame.mouse.get_pos()
                projectile = Projectile(worm.rect.center, target_pos)
                projectiles.add(projectile)

        worms.draw(screen)
        worms.update()
        projectiles.update()  # Update projectiles
        projectiles.draw(screen)  # Draw projectiles

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
