from typing import Tuple, List, Dict
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def to_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def __str__(self) -> str:
        return str(self.to_tuple())

    def __repr__(self) -> str:
        return self.__str__()


class SquareGrid:
    def __init__(self, width: int, height: int, point_weight: Dict[Point, int]):
        self.width = width
        self.height = height
        self.point_weight: Dict[Point, int] = point_weight

    def in_bounds(self, pos: Point) -> bool:
        x, y = pos.to_tuple()

        return 0 <= x < self.width and 0 <= y < self.height

    def adjacent_points(self, pt: Point) -> List[Point]:
        x, y = pt.to_tuple()
        ns = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        bounds_ok = filter(self.in_bounds, map(lambda t: Point(*t), ns))

        return list(bounds_ok)


if __name__ == '__main__':
    p = Point(5, 5)
    print(p)
