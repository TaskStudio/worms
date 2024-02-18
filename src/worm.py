import pygame
from pygame import Surface
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite

from src.weapons import Projectile, Grenade, Rocket


class Worm(Sprite):
    """
    Class for the worms the players will control.
    """

    def __init__(
            self,
            *,
            position: tuple[int, int] | Vector2 = (0, 0),
            scale: float = 0.2,
            name: str = "",
            player: int = 1,
            color=(255, 255, 255),
    ) -> None:
        super().__init__()
        self.frames = self.load_frames('src/assets/spelunky___worms_boggy_b_custom_skin_finished_by_doodlinghitman_da0tnrs-pre.png')
        original_image: Surface = self.frames[0]
        scaled_size = (
            int(original_image.get_width() * scale),
            int(original_image.get_height() * scale),
        )
        self.image: Surface = pygame.transform.scale(original_image, scaled_size)
        self.rect: Rect = self.image.get_rect(center=position)

        self.position = Vector2(position)
        self.velocity = Vector2(0, 0)
        self.speed = 0.2

        self.hp: int = 100
        self.max_hp: int = 100
        self.name = name
        self.player = player
        self.color = color

        self.weapon_class: type[Projectile] | None = None
        self.weapon: Projectile | None = None
        self.aim_target: Vector2 | None = None
        self.weapon_fired: bool = False


        self.current_frame = 0
        self.animation_speed = 0.04  # Time in seconds to wait before switching to next frame
        self.time_since_last_frame = 0
        self.is_moving = False
        self.facing_right = True

    def move_right(self) -> None:
        self.velocity.x = 1
        self.is_moving = True
        self.facing_right = True

    def move_left(self) -> None:
        self.velocity.x = -1
        self.is_moving = True
        self.facing_right = False
    def stop_moving(self) -> None:
        self.velocity.x = 0

    def is_dead(self) -> bool:
        return self.hp <= 0

    def draw_info(self, surface, camera_position, zoom_level):
        font = pygame.font.Font(None, int(24 * zoom_level))
        name_text = font.render(f"{self.name}", True, self.color)

        # Center the name text above the worm
        name_text_pos_x = (
                                  self.rect.centerx - camera_position.x
                          ) * zoom_level - name_text.get_width() / 2
        name_text_pos_y = (
                (self.rect.top - camera_position.y) * zoom_level
                - name_text.get_height()
                - 10 * zoom_level
        )  # Adjust the offset as needed
        name_text_pos = Vector2(name_text_pos_x, name_text_pos_y)
        surface.blit(name_text, name_text_pos)

        # Health bar dimensions and position
        hp_bar_width = 50 * zoom_level  # Width of the health bar; adjust as needed
        hp_bar_height = 5 * zoom_level  # Height of the health bar; adjust as needed

        # Center the health bar above the worm
        hp_bar_pos_x = (
                               self.rect.centerx - camera_position.x
                       ) * zoom_level - hp_bar_width / 2
        hp_bar_pos_y = (
                name_text_pos_y - hp_bar_height - 5 * zoom_level
        )  # Place it above the name text with a small offset
        hp_bar_position = Vector2(hp_bar_pos_x, hp_bar_pos_y)

        # Calculate health ratio
        health_ratio = max(self.hp / self.max_hp, 0)

        # Color for the health bar based on the current health ratio
        health_color = [
            int(red + (green - red) * health_ratio)
            for red, green in zip((255, 0, 0), (0, 255, 0))
        ]

        # Draw the health bar background (the "empty" part of the health bar)
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            (hp_bar_position.x, hp_bar_position.y, hp_bar_width, hp_bar_height),
        )

        # Draw the health part of the health bar
        pygame.draw.rect(
            surface,
            health_color,
            (
                hp_bar_position.x,
                hp_bar_position.y,
                hp_bar_width * health_ratio,
                hp_bar_height,
            ),
        )

    def load_frames(self, image_path):
        scale: float = 5
        num_frames = 12  # Adjust this based on your actual sprite sheet
        sprite_sheet = pygame.image.load(image_path).convert_alpha()
        frame_width = sprite_sheet.get_width() // num_frames
        frame_height = sprite_sheet.get_height()

        frames = []
        for i in range(num_frames):
            # Extract the frame from the sprite sheet
            frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            # Scale the frame
            scaled_frame = pygame.transform.scale(frame, (int(frame_width * scale), int(frame_height * scale)))
            frames.append(scaled_frame)

        return frames

    def animate(self, dt):
        if self.is_moving:  # Only animate if the worm is moving
            self.time_since_last_frame += dt
            if self.time_since_last_frame >= self.animation_speed:
                self.time_since_last_frame -= self.animation_speed
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.update_image()
        else:
            self.time_since_last_frame = 0  # Reset the timer if not moving

    def update_image(self):
        # Flip the frame image if the worm is facing left
        if not self.facing_right:
            self.image = pygame.transform.flip(self.frames[self.current_frame], True, False)
        else:
            self.image = self.frames[self.current_frame]

    def is_charging(self):
        return self.weapon.charging if self.weapon else False

    def set_weapon(self, weapon_class: type[Projectile]):
        self.weapon_class = weapon_class

    def set_weapon_by_name(self, weapon_name):
        if weapon_name == "Grenade":
            self.set_weapon(Grenade)
        elif weapon_name == "Rocket":
            self.set_weapon(Rocket)
        # Additional weapons can be added here

    def reset_weapon(self):
        self.weapon = None
        self.weapon_class = None

    def aim(self, target: Vector2):
        self.aim_target = target

    def charge_weapon(self):
        self.weapon = self.weapon_class()
        self.weapon.set_target(self.aim_target)
        self.weapon.start_charging()

    def release_weapon(self):
        self.weapon.stop_charging()
        self.weapon_fired = True

    def weapon_equipped(self):
        return self.weapon_class is not None

    def update(self, dt, *args, **kwargs):
        self.position += self.velocity * self.speed
        self.rect.center = self.position
        self.animate(dt)

        if self.weapon:
            self.weapon.set_position(self.position)
            if self.weapon.destroyed:
                self.reset_weapon()
