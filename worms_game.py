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
        pygame.init()
        pygame.display.set_caption("WORMS")
        self.screen: Surface = pygame.display.set_mode((g.SCREEN_WIDTH, g.SCREEN_HEIGHT))
        self.running: bool = False

        # Worms setup
        self.player_1_worms, self.player_2_worms = self._generate_starting_worms(
            Vector2(100, g.SCREEN_HEIGHT - 50),  # Adjust starting y to place worms at the bottom
            Vector2(g.SCREEN_WIDTH - 100, g.SCREEN_HEIGHT - 50),
        )
        self.worms_group: Group[Worm] = Group([self.player_1_worms, self.player_2_worms])

        self.worms_queue: Queue[Worm] = Queue(maxsize=len(self.worms_group))
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

        # Camera option
        self.camera_position = Vector2(0, 0)
        self.zoom_level = 1.0
        self.initial_zoom_level = 1.0

    def main(self):
        self.running = True
        while self.running:
            self._handle_events()
            self.update()
        pygame.quit()

    def update(self):
        dead_zone_left = g.SCREEN_WIDTH / 4
        dead_zone_right = 3 * (g.SCREEN_WIDTH / 4)

        extended_boundary_left = -475
        extended_boundary_right = g.SCREEN_WIDTH + 475 - (g.SCREEN_WIDTH / self.zoom_level)
        if self.current_worm.rect.centerx < dead_zone_left:
            desired_camera_x_position = self.current_worm.rect.centerx - g.SCREEN_WIDTH / 4
        elif self.current_worm.rect.centerx > dead_zone_right:
            desired_camera_x_position = self.current_worm.rect.centerx - (g.SCREEN_WIDTH / 4) * 3
        else:
            desired_camera_x_position = self.camera_position.x
        self.camera_position.x = max(extended_boundary_left, min(desired_camera_x_position, extended_boundary_right))
        # Fix the camera's y position as before
        self.camera_position.y = max(0, 0)  # Adjust as needed
        self.screen.fill(color=Color(255, 243, 230))
        self.game_map.draw(self.screen, self.camera_position, self.zoom_level)
        self.worms_group.update()
        self.draw_sprites_with_camera_and_zoom(self.worms_group, self.screen)
        self.projectiles.update()
        self.draw_sprites_with_camera_and_zoom(self.projectiles, self.screen)

        if self.current_projectile and self.current_projectile.charging:
            self.current_projectile.draw_charge(self.screen, self.camera_position, self.zoom_level)

        pygame.display.flip()

    def draw_sprites_with_camera_and_zoom(self, group, surface):
        for sprite in group:
            adjusted_pos = (sprite.rect.topleft - self.camera_position) * self.zoom_level
            scaled_size = (int(sprite.rect.width * self.zoom_level), int(sprite.rect.height * self.zoom_level))
            scaled_image = pygame.transform.scale(sprite.image, scaled_size)
            surface.blit(scaled_image, adjusted_pos)

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
                        self.game_map: MapElement = MapElement(
                            start_x=0, start_y=g.SCREEN_HEIGHT, width=g.SCREEN_WIDTH, height_diff=40
                        )
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Zoom in and out with mouse wheel
                if event.button == g.MOUSE_WHEEL_UP:
                    self.zoom_level = min(self.zoom_level + 0.1, self.initial_zoom_level)
                elif event.button == g.MOUSE_WHEEL_DOWN:
                    self.zoom_level = max(self.zoom_level - 0.1, 0.7)

            if event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_LEFT | pygame.K_RIGHT:
                        self.current_worm.stop_moving()

            # Mouse events
            # Inside the _handle_events method where MOUSEBUTTONDOWN event is handled
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == g.MOUSE_LEFT_CLICK:
                    if not self.current_projectile:
                        # Get the current mouse position in screen coordinates
                        mouse_screen_pos = pygame.mouse.get_pos()

                        # Correctly translate screen position to game world position for the target,
                        # accounting for the camera position and zoom level.
                        mouse_game_world_pos = Vector2(
                            (mouse_screen_pos[0] / self.zoom_level) + self.camera_position.x,
                            (mouse_screen_pos[1] / self.zoom_level) + self.camera_position.y
                        )

                        # Use the worm's position directly for the projectile's start position.
                        # The worm's rect.center is already in game world coordinates and does not require adjustment.
                        start_pos = self.current_worm.rect.center

                        self.current_projectile = Projectile(start_pos, mouse_game_world_pos)
                        self.current_projectile.start_charging()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == g.MOUSE_LEFT_CLICK and self.current_projectile:
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
