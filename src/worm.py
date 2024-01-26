from src.type_defs import Coordinates


class Worm:
    def __init__(self, *, position: Coordinates | tuple[int, int]):
        self.position = (
            position if isinstance(position, Coordinates) else Coordinates(*position)
        )
