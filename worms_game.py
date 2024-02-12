from queue import Queue
from typing import Optional

import pygame
from pygame import Surface, Color, Vector2
from pygame.sprite import Group

import src.globals as g
from src.map import MapElement
from src.projectile import Projectile
from src.worm import Worm


class Game:
    def __init__(self):
        # Pygame setup
        pygame.init()

        pygame.display.set_caption("WORMS")
        self.screen: Surface = pygame.display.set_mode(
            (g.SCREEN_WIDTH, g.SCREEN_HEIGHT)
        )

        self.running: bool = False

        # Worms setup
        self.player_1_worms, self.player_2_worms = self._generate_starting_worms(
            Vector2(100, g.SCREEN_HEIGHT),
            Vector2(g.SCREEN_WIDTH - 100, g.SCREEN_HEIGHT),
        )
        self.worms_group: Group[Worm] = Group(
            [self.player_1_worms, self.player_2_worms]
        )  # Used for game logic and rendering

        self.worms_queue: Queue[Worm] = Queue(
            maxsize=len(self.worms_group)
        )  # Used for turn-based logic
        for worms in zip(self.player_1_worms, self.player_2_worms):
            self.worms_queue.put(worms[0])
            self.worms_queue.put(worms[1])

        self.current_worm: Worm = self.worms_queue.get()
        self.worms_queue.put(self.current_worm)

        # Projectiles setup
        self.projectiles = pygame.sprite.Group()
        self.current_projectile: Optional[Projectile] = None

        # Map setup
        self.game_map: MapElement = MapElement(
            start_x=0, start_y=g.SCREEN_HEIGHT, width=g.SCREEN_WIDTH, height_diff=40
        )


    def main(self):
        self.running = True
        while self.running:
            self._handle_events()
            self.update()

        pygame.quit()

    def update(self):
        self.screen.fill(color=Color(255, 243, 230))

        self.game_map.draw(self.screen)

        self.worms_group.update()
        self.worms_group.draw(self.screen)

        self.projectiles.update()
        self.projectiles.draw(self.screen)

        if self.current_projectile and self.current_projectile.charging:
            self.current_projectile.draw_charge(self.screen)

        # Window refresh
        pygame.display.flip()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Key down events
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        self.running = False
                        pygame.quit()
                    case pygame.K_LEFT:
                        self.current_worm.move_left()
                    case pygame.K_RIGHT:
                        self.current_worm.move_right()
                    case pygame.K_SPACE:
                        self.current_worm.stop_moving()
                        self.current_worm = self.worms_queue.get()
                        self.worms_queue.put(self.current_worm)
                    case pygame.K_r:
                        self.game_map = MapElement(
                            start_x=0, start_y=720, width=1080, height_diff=100
                        )

            if event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_LEFT | pygame.K_RIGHT:
                        self.current_worm.stop_moving()

            # Mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.current_projectile:
                    self.current_projectile = Projectile(
                        self.current_worm.rect.center, pygame.mouse.get_pos()
                    )
                    self.current_projectile.start_charging()
            if event.type == pygame.MOUSEBUTTONUP and self.current_projectile:
                self.current_projectile.stop_charging()
                self.projectiles.add(self.current_projectile)
                self.current_projectile = None

    @staticmethod
    def _generate_starting_worms(
        player_1_start_position: Vector2, player_2_start_position: Vector2
    ) -> tuple[Group, Group]:
        player_1_worms: Group[Worm] = Group(
            [
                Worm(position=player_1_start_position + Vector2(i * 100, 0))
                for i in range(g.WORMS_PER_PLAYER)
            ]
        )
        player_2_worms: Group[Worm] = Group(
            [
                Worm(position=player_2_start_position - Vector2(i * 100, 0))
                for i in range(g.WORMS_PER_PLAYER)
            ]
        )
        return player_1_worms, player_2_worms



if __name__ == "__main__":
    game = Game()
    game.main()
