from pygame.time import Clock

from src.physics import Rigidbody


class PhysicsManager:
    def __init__(
        self, game_clock: Clock, rigidbodies: list[Rigidbody] | None = None
    ) -> None:
        self.rigidbodies: list[Rigidbody] = rigidbodies if rigidbodies else []
        self.game_clock: Clock = game_clock

    def add_rigidbody(self, rb: Rigidbody) -> None:
        self.rigidbodies.append(rb)

    def update(self) -> None:
        for rb in self.rigidbodies:
            rb.physics_update(self.game_clock.get_time())
