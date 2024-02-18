from pygame import Vector2

import src.globals as g


class Rigidbody:
    def __init__(self, mass=1, position=Vector2(0, 0), velocity=Vector2(0, 0)):
        self.mass = mass
        self.gravity = g.GRAVITY
        self.position = position
        self.velocity = velocity
        self.forces = Vector2(0, 0)

    def add_force(self, force):
        self.forces += force / self.mass

    def set_force(self, force):
        self.forces = force / self.mass

    def clear_horizontal_forces(self):
        self.forces.x = 0

    def physics_update(self, delta_time):
        # Apply gravity as a constant force
        self.add_force(Vector2(0, self.mass * self.gravity))
        # Update velocity with accumulated forces
        self.velocity += self.forces * delta_time
        # Update position with velocity
        self.position += self.velocity * delta_time
