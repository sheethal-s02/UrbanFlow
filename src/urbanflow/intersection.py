from dataclasses import dataclass


@dataclass(frozen=True)
class Intersection:
    id: int
    x: float
    y: float