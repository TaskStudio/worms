from pygame import Vector2
from pygame.time import Clock

from src.physics import Rigidbody


class PhysicsManager:
    def __init__(
        self,
        *,
        game_clock: Clock,
        rigidbodies: list[Rigidbody] | None = None,
        wind: Vector2 = Vector2(0, 0),
    ) -> None:
        self.rigidbodies: list[Rigidbody] = rigidbodies if rigidbodies else []
        self.game_clock: Clock = game_clock
        self.wind: Vector2 = wind

    def add_rigidbody(self, rb: Rigidbody) -> None:
        self.rigidbodies.append(rb)

    def update(self) -> None:
        for rb in self.rigidbodies:
            rb.physics_update(self.game_clock.get_time())
            if rb.affected_by_wind:
                rb.apply_forces(self.wind)
