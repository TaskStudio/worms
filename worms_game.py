from queue import Queue
from typing import Optional

import pygame
from pygame import Surface, Color, Vector2
from pygame.sprite import Group
from pygame.time import Clock

import src.globals as g
from src.Timer import Timer
from src.map import MapElement
from src.worm import Worm
from src.weapons import Grenade, Rocket
from src.forces import Forces


class Game:
    """
    Main class for the game.

    ...

    Attributes
    ----------
    screen : Surface
        The game window.
    running : bool
        The game loop state.
    game_clock : Clock
        The general game clock.

    player_timer : Timer
        The timer for the current player's turn. When it reaches 0, the turn changes.

    player_1_worms, player_2_worms : Group
        The worms for each player.
    worms_group : Group
        A group containing all the worms, used for game logic and rendering.
    worms_queue : Queue
        A queue containing all the worms, used for turn management.
    current_worm : Worm
        The worm currently playing.

    projectiles : Group
        A group containing all the projectiles.

    game_map : MapElement
        The main map element.
    """

    def __init__(self):
        # Pygame setup
        pygame.init()
        pygame.display.set_caption("WORMS")

        self.screen: Surface = pygame.display.set_mode(
            (g.SCREEN_WIDTH, g.SCREEN_HEIGHT)
        )
        self.running: bool = False
        self.game_clock: Clock = Clock()

        self.player_timer = Timer(g.PLAYER_TURN_DURATION)

        # Forces setup
        self.wind = Forces.generate_wind()

        # Worms setup
        self.player_1_worms, self.player_2_worms = self._generate_starting_worms(
            Vector2(100, g.SCREEN_HEIGHT - 50),  # Adjust starting y to place worms at the bottom
            Vector2(g.SCREEN_WIDTH - 100, g.SCREEN_HEIGHT - 50),
        )
        self.worms_group: Group[Worm] = Group(
            [self.player_1_worms, self.player_2_worms]
        )

        self.worms_queue: Queue[Worm] = Queue(maxsize=len(self.worms_group))
        for worms in zip(self.player_1_worms, self.player_2_worms):
            self.worms_queue.put(worms[0])
            self.worms_queue.put(worms[1])

        self.current_worm: Worm = self.worms_queue.get()
        self.worms_queue.put(self.current_worm)

        # Projectiles setup
        self.projectiles = pygame.sprite.Group()
        self.weapon_message = "Weapon: None"

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
        self.player_timer.start()
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

        Forces.draw_wind(self.screen, self.wind)
        Forces.draw_wind_arrow(self.screen, self.wind, (self.screen.get_width() - 50, 50))

        for projectile in self.projectiles:
            projectile.check_collision(self.worms_group, current_worm=self.current_worm)

        self.worms_group.update()
        self.draw_sprites_with_camera_and_zoom(self.worms_group, self.screen)
        self.projectiles.update()
        self.draw_sprites_with_camera_and_zoom(self.projectiles, self.screen)

        if self.current_worm.weapon_equipped():
            self.current_worm.aim(pygame.mouse.get_pos() + self.camera_position)
            if self.current_worm.is_charging():
                self.current_worm.weapon.draw(self.screen, self.camera_position, self.zoom_level)

        # Clock and window refresh
        self.game_clock.tick(g.FPS)

        self.player_timer.update()
        self.player_timer.draw(self.screen, Vector2(g.SCREEN_WIDTH - 100, 50))
        if self.player_timer.is_finished():
            self.change_turn()

        # Afficher le message de l'arme actuelle
        font = pygame.font.Font(None, 36)
        text = font.render(self.weapon_message, True, (10, 10, 10))
        self.screen.blit(text, (10, 10))

        # Window refresh
        pygame.display.flip()

    def draw_sprites_with_camera_and_zoom(self, group, surface):
        for sprite in group:
            adjusted_pos = (sprite.rect.topleft - self.camera_position) * self.zoom_level
            scaled_size = (int(sprite.rect.width * self.zoom_level), int(sprite.rect.height * self.zoom_level))
            scaled_image = pygame.transform.scale(sprite.image, scaled_size)
            surface.blit(scaled_image, adjusted_pos)

            if isinstance(sprite, Worm):
                sprite.draw_info(surface, self.camera_position, self.zoom_level)

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
                        self.change_turn()
                    case pygame.K_r:
                        self.game_map: MapElement = MapElement(
                            start_x=0, start_y=g.SCREEN_HEIGHT, width=g.SCREEN_WIDTH, height_diff=40
                        )
                    case pygame.K_1:
                        self.current_worm.set_weapon(Grenade)
                        self.weapon_message = "Weapon: Grenade"
                    case pygame.K_2:
                        self.current_worm.set_weapon(Rocket)
                        self.weapon_message = "Weapon: Rocket"

            if event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_LEFT | pygame.K_RIGHT:
                        self.current_worm.stop_moving()

            # Mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_worm.weapon_equipped():
                    self.current_worm.charge_weapon()
                    self.projectiles.add(self.current_worm.weapon)
            if event.type == pygame.MOUSEBUTTONUP:
                if self.current_worm.is_charging():
                    self.current_worm.release_weapon()

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:  # Scroll up to zoom in
                    self.zoom_level = min(self.zoom_level + 0.1, self.initial_zoom_level)
                elif event.y < 0:  # Scroll down to zoom out
                    self.zoom_level = max(self.zoom_level - 0.1, 0.5)  # Adjust the minimum zoom level as needed

    def change_turn(self):
        self.current_worm.stop_moving()

        for _ in range(self.worms_queue.qsize()):
            worm = self.worms_queue.get()
            if worm.is_dead():  # If the worm is in the queue and dead, we remove it
                worm.kill()
            else:
                self.worms_queue.put(worm)

        self.current_worm = self.worms_queue.get()
        self.worms_queue.put(self.current_worm)

        self.player_timer.reset()
        self.player_timer.start()

    def _generate_starting_worms(self, player_1_start_position: Vector2, player_2_start_position: Vector2) -> tuple[
        Group, Group]:
        player_1_worms: Group[Worm] = Group(
            [
                Worm(position=player_1_start_position + Vector2(i * 100, 0), name=f"Worm {i + 1}", player=1,
                     color=(0, 0, 255))
                for i in range(g.WORMS_PER_PLAYER)
            ]
        )
        player_2_worms: Group[Worm] = Group(
            [
                Worm(position=player_2_start_position - Vector2(i * 100, 0), name=f"Worm {i + 1}", player=2,
                     color=(255, 0, 0))
                for i in range(g.WORMS_PER_PLAYER)
            ]
        )
        return player_1_worms, player_2_worms


if __name__ == "__main__":
    game = Game()
    game.main()
