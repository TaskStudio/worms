import pygame
from pygame import Surface, Color


def main() -> None:
    pygame.init()

    pygame.display.set_caption("WORMS")
    screen: Surface = pygame.display.set_mode((1080, 720))

    running: bool = True

    while running:
        screen.fill(color=Color(255, 243, 230))

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


main()
