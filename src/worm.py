import pygame
from pygame import Surface
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite

import src.globals as g
from src.rigidbody import (
    Rigidbody,
)  # Make sure this import matches your project structure
from src.weapons import Projectile



class Worm(Sprite, Rigidbody):
    """
    Class for the worms the players will control.
    """

    def __init__(self, *, position: tuple[int, int] | Vector2 = (0, 0), scale: float = 0.2) -> None:
        # Setup for the sprite class
        Sprite.__init__(self)
        # Initialize Rigidbody with mass, gravity, and initial position
        Rigidbody.__init__(self, mass=g.WORMS_MASS, position=position)

        original_image: Surface = pygame.image.load("src/assets/worm.png")
        scaled_size = (int(original_image.get_width() * scale), int(original_image.get_height() * scale))
        self.image: Surface = pygame.transform.scale(original_image, scaled_size)        self.rect: Rect = self.image.get_rect(center=position)

        self.move_force = 12000
        self.hp: int = 100
        self.max_hp: int = 100

        self.is_moving = False
        
        self.weapon_class: type[Projectile] | None = None
        self.weapon: Projectile | None = None
        self.aim_target: Vector2 | None = None

    def move_right(self):
        if not self.is_moving:
            self.set_force(Vector2(self.move_force, 0))
            self.is_moving = True

    def move_left(self):
        if not self.is_moving:
            self.set_force(Vector2(-self.move_force, 0))
            self.is_moving = True
            
    def stop_moving(self):
        self.is_moving = False
        super().clear_horizontal_forces()

    def is_dead(self) -> bool:
        return self.hp <= 0

    def is_charging(self):
        return self.weapon.charging if self.weapon else False

    def set_weapon(self, weapon_class: type[Projectile]):
        self.weapon_class = weapon_class

    def aim(self, target: Vector2):
        self.aim_target = target

    def charge_weapon(self):
        self.weapon = self.weapon_class()
        self.weapon.set_target(self.aim_target)
        self.weapon.start_charging()

    def release_weapon(self):
        self.weapon.stop_charging()

    def weapon_equipped(self):
        return self.weapon_class is not None

    def update(self, *args, **kwargs):
        self.position += self.velocity * self.speed
        self.rect.center = self.position

        if self.weapon:
            self.weapon.set_position(self.position)
