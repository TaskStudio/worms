import math

from pygame import Vector2

import src.globals as g


class Rigidbody:
    def __init__(self, mass=1, position=Vector2(0, 0), velocity=Vector2(0, 0)):
        self.mass = mass
        self.gravity = g.g
        self.position = position
        self.initial_velocity = velocity
        self.start_pos = position
        self.time = 0

    def apply_forces(self, force):
        self.start_pos = self.position.copy()
        self.time = 0

        angle = math.radians(force.angle_to(Vector2(1, 0)))
        x_force = force.magnitude() * math.cos(angle)
        y_force = -force.magnitude() * math.sin(angle)
        self.initial_velocity = Vector2(x_force, y_force)

    def set_velocity(self, velocity):
        self.initial_velocity = velocity

    def clear_horizontal_velocity(self):
        self.initial_velocity.x = 0

    def physics_update(self, delta_time):
        delta_time /= 1000
        self.time += delta_time
        self.position.x = self.initial_velocity.x * self.time + self.start_pos.x
        self.position.y = (
            self.initial_velocity.y * self.time
            + self.start_pos.y
            + (0.5 * self.gravity * self.time**2)
        )
        if self.position.y > g.SCREEN_HEIGHT:
            self.position.y = g.SCREEN_HEIGHT
