import pygame
from pygame import Surface
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite

import src.globals as g
from src.rigidbody import (
    Rigidbody,
)  # Make sure this import matches your project structure


class Worm(Sprite, Rigidbody):
    """
    Class for the worms the players will control.
    """

    def __init__(self, *, position: tuple[int, int] | Vector2 = (0, 0)) -> None:
        # Setup for the sprite class
        Sprite.__init__(self)
        # Initialize Rigidbody with mass, gravity, and initial position
        Rigidbody.__init__(self, mass=g.WORMS_MASS, position=position)

        self.image: Surface = pygame.image.load("src/assets/worm.png")
        self.rect: Rect = self.image.get_rect(center=position)

        self.move_force = 12000
        self.hp: int = 100
        self.max_hp: int = 100
        self.current_worm: bool = False

        self.is_moving = False

    def move_right(self):
        # Apply a force to the right only if not currently moving
        if not self.is_moving:
            self.set_force(Vector2(self.move_force, 0))
            self.is_moving = True

    def move_left(self):
        # Apply a force to the left only if not currently moving
        if not self.is_moving:
            self.set_force(Vector2(-self.move_force, 0))
            self.is_moving = True

    def update(self, delta_time):
        if self.is_moving:
            # Allow the physics update to proceed with the applied force
            Rigidbody.update(self, delta_time)
            self.velocity.x = 0
        else:
            # Regular physics update without additional movement
            Rigidbody.update(self, delta_time)

        # Update sprite position to match the physics position
        self.rect.center = self.position

    def stop_moving(self):
        # Additional logic to stop the worm, if needed for future functionality
        self.is_moving = False
        super().clear_horizontal_forces()

    def is_dead(self):
        return self.hp <= 0
