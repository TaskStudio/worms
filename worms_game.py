from queue import Queue

import pygame
from pygame import Surface, Color, Vector2
from pygame.sprite import Group
from pygame.time import Clock

import src.globals as g
from src.button import Button
from src.map import MapElement
from src.physics import PhysicsManager
from src.physics.forces import Forces
from src.timer import Timer
from src.weapons import Grenade, Rocket
from src.weapons.weapon_bar import WeaponBar
from src.worm import Worm


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

        # Physics setup
        self.wind = Forces.generate_wind()
        self.physics_manager = PhysicsManager(
            game_clock=self.game_clock, wind=self.wind
        )

        # Worms setup
        self.player_1_worms, self.player_2_worms = self._generate_starting_worms(
            Vector2(
                100, g.SCREEN_HEIGHT - 200
            ),  # Adjust starting y to place worms at the bottom
            Vector2(g.SCREEN_WIDTH - 100, g.SCREEN_HEIGHT - 200),
        )
        self.worms_group: Group[Worm] = Group(
            [self.player_1_worms, self.player_2_worms]
        )

        self.worms_queue: Queue[Worm] = Queue(maxsize=len(self.worms_group))
        for worms in zip(self.player_1_worms, self.player_2_worms):
            self.worms_queue.put(worms[0])
            self.worms_queue.put(worms[1])
            self.physics_manager.add_rigidbody(worms[0].rb)
            self.physics_manager.add_rigidbody(worms[1].rb)

        self.current_worm: Worm = self.worms_queue.get()
        self.worms_queue.put(self.current_worm)

        # Projectiles setup
        self.projectiles = pygame.sprite.Group()
        self.weapon_message = "Weapon: None"
        self.current_weapon = None

        # Map setup
        self.game_map: MapElement = MapElement(
            start_x=0, start_y=g.SCREEN_HEIGHT, width=g.SCREEN_WIDTH, height_diff=40
        )

        # Camera option
        self.camera_position = Vector2(0, 0)
        self.zoom_level = 1.0
        self.initial_zoom_level = 1.0

        self.resume_image = pygame.image.load(
            "src/assets/button_resume.png"
        ).convert_alpha()
        self.quit_image = pygame.image.load(
            "src/assets/button_quit.png"
        ).convert_alpha()

        # Calculate the button height dynamically from the image
        resume_button_height = self.resume_image.get_height()
        quit_button_height = self.quit_image.get_height()

        # Position the resume button centered on the screen
        self.resume_button = Button(
            g.SCREEN_WIDTH / 2 - self.resume_image.get_width() / 2,
            g.SCREEN_HEIGHT / 2 - resume_button_height / 2,
            self.resume_image,
            1,
        )

        # Position the quit button below the resume button with a dynamic gap
        gap = 20  # Define a gap between the buttons
        self.quit_button = Button(
            g.SCREEN_WIDTH / 2 - self.quit_image.get_width() / 2,
            g.SCREEN_HEIGHT / 2 + quit_button_height / 2 + gap,
            self.quit_image,
            1,
        )
        self.game_paused = True

        weapon_image_paths = ["src/assets/W4_Grenade.webp", "src/assets/Bazooka.webp"]
        weapon_identifiers = ["Grenade", "Rocket"]
        self.weapon_bar = WeaponBar(
            (g.SCREEN_WIDTH // 2, 10), weapon_image_paths, weapon_identifiers
        )

    def main(self):
        self.running = True
        self.player_timer.start()
        while self.running:
            self._handle_events()
            self.update()

        pygame.quit()

    def update(self):
        if self.game_paused:
            self.screen.fill((0, 0, 0))  # Clear the screen
            if self.resume_button.draw(self.screen):
                self.game_paused = False
            if self.quit_button.draw(self.screen):
                self.running = False
        else:
            dead_zone_left = g.SCREEN_WIDTH / 4
            dead_zone_right = 3 * (g.SCREEN_WIDTH / 4)

            extended_boundary_left = -475
            extended_boundary_right = (
                g.SCREEN_WIDTH + 475 - (g.SCREEN_WIDTH / self.zoom_level)
            )
            if self.current_worm.rect.centerx < dead_zone_left:
                desired_camera_x_position = (
                    self.current_worm.rect.centerx - g.SCREEN_WIDTH / 4
                )
            elif self.current_worm.rect.centerx > dead_zone_right:
                desired_camera_x_position = (
                    self.current_worm.rect.centerx - (g.SCREEN_WIDTH / 4) * 3
                )
            else:
                desired_camera_x_position = self.camera_position.x
            self.camera_position.x = max(
                extended_boundary_left,
                min(desired_camera_x_position, extended_boundary_right),
            )
            # Fix the camera's y position as before
            self.camera_position.y = max(0, 0)  # Adjust as needed

            if self.current_weapon and self.current_weapon.launched:
                self.camera_position.x = max(
                    extended_boundary_left,
                    min(
                        self.current_weapon.rect.centerx - g.SCREEN_WIDTH / 2,
                        extended_boundary_right,
                    ),
                )
                self.camera_position.y = max(
                    0, self.current_weapon.rect.centery - g.SCREEN_HEIGHT / 2
                )

            self.screen.fill(color=Color(255, 243, 230))

            self.game_map.draw(self.screen, self.camera_position, self.zoom_level)
            self.draw_worm_queue()

            self.weapon_bar.draw(self.screen)
            # Update the current worm's weapon based on the selected weapon in the weapon bar
            selected_weapon_name = self.weapon_bar.get_selected_weapon()

            Forces.draw_wind(self.screen, self.wind)
            Forces.draw_wind_arrow(
                self.screen, self.wind, (self.screen.get_width() - 75, 25)
            )
            self.physics_manager.update()

            for projectile in self.projectiles:
                projectile.check_collision(
                    self.worms_group, current_worm=self.current_worm
                )

            self.worms_group.update()
            self.draw_sprites_with_camera_and_zoom(self.worms_group, self.screen)
            self.projectiles.update()
            self.draw_sprites_with_camera_and_zoom(self.projectiles, self.screen)

            if self.current_weapon:
                self.current_weapon.draw(
                    self.screen, self.camera_position, self.zoom_level
                )

            # Clock and window refresh
            self.game_clock.tick(g.FPS)

            self.player_timer.update()
            self.player_timer.draw(self.screen, Vector2(g.SCREEN_WIDTH - 100, 50))
            if self.player_timer.get_countdown() <= 0:
                self.change_turn()

            # Afficher le message de l'arme actuelle
            font = pygame.font.Font(None, 36)
            text = font.render(self.weapon_message, True, (10, 10, 10))
            self.screen.blit(text, (10, 10))

        # Window refresh
        pygame.display.flip()

    def draw_sprites_with_camera_and_zoom(self, group, surface):
        for sprite in group:
            adjusted_pos = (
                sprite.rect.topleft - self.camera_position
            ) * self.zoom_level
            scaled_size = (
                int(sprite.rect.width * self.zoom_level),
                int(sprite.rect.height * self.zoom_level),
            )
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
                    case pygame.K_1:
                        if not self.current_worm.weapon_fired:
                            self.current_weapon = Grenade()
                            self.weapon_message = "Weapon: Grenade"
                            self.weapon_bar.selected_weapon_index = 0
                    case pygame.K_2:
                        if len(self.weapon_bar.weapon_identifiers) > 1:
                            self.current_weapon = Rocket()
                            self.weapon_message = "Weapon: Rocket"
                            self.weapon_bar.selected_weapon_index = 1

            if event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_LEFT | pygame.K_RIGHT:
                        self.current_worm.stop_moving()

            # Mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_weapon and not self.current_worm.weapon_fired:
                    self.current_weapon.set_position(
                        Vector2(self.current_worm.rect.center)
                    )
                    self.current_weapon.set_target(Vector2(pygame.mouse.get_pos()))
                    self.current_weapon.start_charging()
                    self.projectiles.add(self.current_weapon)
            if event.type == pygame.MOUSEBUTTONUP:
                if self.current_weapon and not self.current_worm.weapon_fired:
                    self.current_weapon.stop_charging()
                    self.current_worm.weapon_fired = True
                    self.player_timer.set_duration(5)
                    self.player_timer.reset()
                    self.player_timer.start()

                    self.physics_manager.add_rigidbody(self.current_weapon.rb)

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:  # Scroll up to zoom in
                    self.zoom_level = min(
                        self.zoom_level + 0.1, self.initial_zoom_level
                    )
                elif event.y < 0:  # Scroll down to zoom out
                    self.zoom_level = max(
                        self.zoom_level - 0.1, 0.5
                    )  # Adjust the minimum zoom level as needed

    def draw_worm_queue(self):
        font = pygame.font.Font(None, 24)
        queue_display_position = (10, 50)  # Top-left corner, adjust as needed
        spacing = 30  # Vertical spacing between names

        # Display a title for the queue
        title_text = font.render("Next:", True, (255, 255, 255))
        self.screen.blit(title_text, queue_display_position)

        # Create a temporary queue to hold and display the next few worms without altering the main queue
        temp_queue = (
            self.worms_queue.queue.copy()
        )  # Assuming Python 3.7+, for older versions use list(self.worms_queue.queue)
        temp_queue.rotate(
            0
        )  # Adjust based on your current worm handling, to not show the current worm as next

        # Limit the number of worms shown in the queue
        max_display = 3
        count = 0

        for worm in list(temp_queue):
            if count >= max_display:
                break
            worm_name = worm.name
            color = worm.color
            text = font.render(worm_name, True, color)
            self.screen.blit(
                text,
                (
                    queue_display_position[0],
                    queue_display_position[1] + spacing * (count + 1),
                ),
            )
            count += 1

    def change_turn(self):
        self.current_worm.stop_moving()
        self.current_worm.weapon_fired = False
        self.current_weapon = None

        for _ in range(self.worms_queue.qsize()):
            worm = self.worms_queue.get()
            if worm.is_dead():  # If the worm is in the queue and dead, we remove it
                worm.kill()
            else:
                self.worms_queue.put(worm)

        self.current_worm = self.worms_queue.get()
        self.worms_queue.put(self.current_worm)

        self.player_timer.set_duration(g.PLAYER_TURN_DURATION)
        self.player_timer.reset()
        self.player_timer.start()

        self.wind = Forces.generate_wind()

    def _generate_starting_worms(
        self, player_1_start_position: Vector2, player_2_start_position: Vector2
    ) -> tuple[Group, Group]:
        player_1_worms: Group[Worm] = Group(
            [
                Worm(
                    position=player_1_start_position + Vector2(i * 100, 0),
                    name=f"Worm {i + 1}",
                    player=1,
                    color=(0, 0, 255),
                )
                for i in range(g.WORMS_PER_PLAYER)
            ]
        )
        player_2_worms: Group[Worm] = Group(
            [
                Worm(
                    position=player_2_start_position - Vector2(i * 100, 0),
                    name=f"Worm {i + 1}",
                    player=2,
                    color=(255, 0, 0),
                )
                for i in range(g.WORMS_PER_PLAYER)
            ]
        )
        return player_1_worms, player_2_worms


if __name__ == "__main__":
    game = Game()
    game.main()
