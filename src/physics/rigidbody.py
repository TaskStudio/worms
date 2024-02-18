import math

from pygame import Vector2

import src.globals as g


class Rigidbody:
    def __init__(self, mass=1, position=Vector2(0, 0), velocity=Vector2(0, 0)):
        self.mass = mass
        self.gravity = g.g
        self.position = position
        self.initial_velocity = velocity
        self.start_pos = Vector2()
        self.time = 0

    def apply_forces(self, force):
        self.start_pos = self.position.copy()
        self.time = 0

        angle = math.radians(force.angle_to(Vector2(1, 0)))
        self.initial_velocity.x = force.magnitude() * math.cos(angle)
        self.initial_velocity.y = -force.magnitude() * math.sin(angle)

    def set_velocity(self, velocity):
        self.initial_velocity = velocity

    def clear_horizontal_velocity(self):
        self.initial_velocity.x = 0

    def physics_update(self, delta_time):
        # if self.position.y >= g.SCREEN_HEIGHT - 100:
        #     self.velocity.y = 0

        delta_time /= 1000
        self.time += delta_time
        self.position.x = self.initial_velocity.x * self.time + self.start_pos.x
        self.position.y = (
            self.initial_velocity.y * self.time
            + self.start_pos.y
            + (0.5 * self.gravity * self.time**2)
        )
