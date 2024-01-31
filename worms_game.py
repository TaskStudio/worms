import pygame
from pygame import Surface, Color

from src.map import MapElement
from src.worm import Worm


def main() -> None:
    pygame.init()

    pygame.display.set_caption("WORMS")
    screen: Surface = pygame.display.set_mode((1080, 720))

    running: bool = True

    worm: Worm = Worm(position=(200, 200))

    worms = pygame.sprite.Group(worm)

    map: MapElement = MapElement(start_x=0, start_y=720, width=1080, height_diff=40)

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
                    case pygame.K_r:
                        map = MapElement(start_x=0, start_y=720, width=1080, height_diff=100)

            if event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_LEFT | pygame.K_RIGHT:
                        worm.stop_moving()


main()
