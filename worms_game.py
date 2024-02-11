from queue import Queue
from typing import Optional

import pygame
from pygame import Surface, Color, Vector2
from pygame.sprite import Group, GroupSingle

import src.globals as g
from src.worm import Worm
from src.projectile import Projectile


def main() -> None:
    # Pygame setup
    pygame.init()

    pygame.display.set_caption("WORMS")
    screen: Surface = pygame.display.set_mode((g.SCREEN_WIDTH, g.SCREEN_HEIGHT))

    running: bool = True

    # Worms setup
    player_1_start_position: Vector2 = Vector2(100, g.SCREEN_HEIGHT)
    player_2_start_position: Vector2 = Vector2(g.SCREEN_WIDTH - 100,  g.SCREEN_HEIGHT)

    player_1_worms: Group[Worm] = Group([Worm(position=player_1_start_position + Vector2(i*100, 0)) for i in range(g.WORMS_PER_PLAYER)])
    player_2_worms: Group[Worm] = Group([Worm(position=player_2_start_position - Vector2(i*100, 0)) for i in range(g.WORMS_PER_PLAYER)])

    worms_group: Group[Worm] = Group([player_1_worms, player_2_worms])
    
    projectiles = pygame.sprite.Group()
    max_charge_duration: int = 3000
    current_projectile: Optional[Projectile] = None

    worms_queue: Queue[Worm] = Queue(maxsize=len(worms_group))
    for worms in zip(player_1_worms, player_2_worms):
        worms_queue.put(worms[0])
        worms_queue.put(worms[1])

    current_worm: Worm = worms_queue.get()
    worms_queue.put(current_worm)

    # Game loop
    while running:
        screen.fill(color=Color(255, 243, 230))

        worms_group.draw(screen)
        worms_group.update()

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
                        current_worm.move_left()
                    case pygame.K_RIGHT:
                        current_worm.move_right()
                    case pygame.K_SPACE:
                        current_worm.stop_moving()
                        current_worm = worms_queue.get()
                        worms_queue.put(current_worm)

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
                match event.key:
                    case pygame.K_LEFT | pygame.K_RIGHT:
                        current_worm.stop_moving()

        if current_projectile and current_projectile.charging:
            current_projectile.draw_charge(screen, max_charge_duration)

        projectiles.update()
        projectiles.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
