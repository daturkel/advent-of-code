#!/usr/bin/env python3

import sys
from time import perf_counter

Point = tuple[int, int]


class Grid:
    points: list[list[Point]]

    def __init__(
        self,
        points: list[list[Point]],
        max_y: int,
        source: Point,
    ):
        self.points = points
        self.source = source
        self.max_y = max_y
        self.width = (self.max_y + 2) * 2 + 1
        # our arrays are technically wrapping around, so we keep track of offset for printing
        self.offset = (self.max_y + 2) - self.source[0]
        self.clear_grid()

    # (re)set the grid, including all lines of rock
    def clear_grid(self):
        self._grid = [["." for i in range(self.width)] for j in range(max_y + 1)]
        self.set(self.source, "+")
        self.set_points()

    # print out the grid
    def show(self):
        for row in self._grid:
            print("".join(row[-self.offset :] + row[: -self.offset]))

    # add a floor to the grid 2 below current bottom
    def add_floor(self):
        self._grid.append(["." for i in range(self.width)])
        self._grid.append(["#" for i in range(self.width)])

    # can a point fall here? true if yes, false if no, None if we fall of the board
    def can_fall(self, point: Point) -> bool | None:
        x, y = point
        try:
            new_pt = self._grid[y][x]
        except IndexError:
            return None
        return new_pt == "."

    # find where to fall next, or None if we fall off the board
    def find_next(self, point: Point) -> Point | None:
        x, y = point

        for pt in [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]:
            can_fall = self.can_fall(pt)
            if can_fall:
                return pt
            elif can_fall is None:
                return None

        # stay where we are
        return point

    # set a coordinate
    def set(self, point: Point, symbol: str):
        x, y = point
        self._grid[y][x] = symbol

    # set initial points from instructions
    def set_points(self):
        for line in self.points:
            for i in range(len(line) - 1):
                (x1, y1), (x2, y2) = line[i : i + 2]
                if x1 != x2:
                    # left, right
                    l, r = sorted([x1, x2])
                    x = l
                    while x <= r:
                        self.set((x, y1), "#")
                        x += 1
                else:
                    # bottom, top
                    b, t = sorted([y1, y2])
                    y = b
                    while y <= t:
                        self.set((x1, y), "#")
                        y += 1

    # drop sand once from source, return whether or not we can keep dropping
    def drop_one(self) -> bool:
        point = self.source
        next_point = self.find_next(point)
        while next_point:
            if next_point == point:
                self.set(point, "o")
                break
            point = next_point
            next_point = self.find_next(point)

        return (next_point is not None) and (point != self.source)

    # drop sand for as long as we can, return how many times we could drop
    def drop(self, verbose=False) -> int:
        dropped = 0
        while True:
            keep_dropping = self.drop_one()
            if not keep_dropping:
                break
            dropped += 1
            if verbose:
                self.show()
                print(dropped)
        return dropped


def parse_input(lines: list[str]) -> tuple[list[list[Point]], int, int]:
    points = []
    min_x = 1000
    max_y = 0
    for line in lines:
        line_points = []
        points_str = line.split(" -> ")
        for point_str in points_str:
            x_str, y_str = point_str.split(",")
            x, y = int(x_str), int(y_str)
            min_x = min(min_x, x)
            max_y = max(max_y, y)
            line_points.append((x, y))
        points.append(line_points)

    for i in range(len(points)):
        points[i] = [(point[0] - min_x, point[1]) for point in points[i]]

    return points, min_x, max_y


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = [line.rstrip() for line in file.readlines()]

    tic = perf_counter()

    points, min_x, max_y = parse_input(lines)
    grid = Grid(points, max_y, (500 - min_x, 0))
    num_dropped_a = grid.drop()
    # grid.show()

    grid.clear_grid()
    grid.add_floor()
    # add 1 to include the sand that covers the source
    num_dropped_b = grid.drop() + 1
    # grid.show()

    toc = perf_counter()
    time_us = round((toc - tic), 1)

    print(f"{num_dropped_a=}, {num_dropped_b=} ({time_us}s)")
