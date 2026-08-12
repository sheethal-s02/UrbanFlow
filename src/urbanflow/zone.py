from dataclasses import dataclass

from .intersection import Intersection


@dataclass
class Zone:
    name: str
    intersections: list[Intersection]
    attraction: float = 1.0

    def choose_intersection(
        self,
    ) -> Intersection:

        import random

        return random.choice(
            self.intersections
        )