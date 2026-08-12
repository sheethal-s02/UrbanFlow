from dataclasses import dataclass
import math


@dataclass
class Road:

    id: int
    start: object
    end: object

    speed_limit: float = 50.0

    # ========================================================
    # ROAD LENGTH
    # ========================================================

    def get_length(
        self,
    ) -> float:

        dx = (
            self.end.x
            - self.start.x
        )

        dy = (
            self.end.y
            - self.start.y
        )

        return math.sqrt(
            dx * dx
            + dy * dy
        )