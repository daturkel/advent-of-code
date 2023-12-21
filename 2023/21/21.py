import sys
from collections import deque
from time import perf_counter

Point = tuple[int, int]


class Grid:
    def __init__(self, lines: list[str]):
        self._grid = {}
        self.start = (0, 0)
        self.width = len(lines[0])
        self.height = len(lines)
        for x, row in enumerate(lines):
            for y, char in enumerate(row):
                self._grid[(x, y)] = char
                if char == "S":
                    self.start = (x, y)

    def neighbors(self, point: Point, cache={}) -> list[Point]:
        x, y = point
        try:
            return cache[point]
        except KeyError:
            pass

        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if self._grid.get((x + dx, y + dy), "#") != "#":
                neighbors.append((x + dx, y + dy))

        cache[point] = neighbors

        return neighbors

    def neighbors_looping(self, point: Point, cache={}) -> list[Point]:
        x, y = point
        try:
            return cache[point]
        except KeyError:
            pass

        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if (
                self._grid.get(((x + dx) % self.width, (y + dy) % self.height), "#")
                != "#"
            ):
                neighbors.append((x + dx, y + dy))

        cache[point] = neighbors

        return neighbors


def solve(lines: list[str]) -> tuple[int, int]:
    grid = Grid(lines)
    queue_a: deque[tuple[Point, int]] = deque([(grid.start, 0)])
    n_steps_a = 64
    final_spots_a = set()
    visited_a = set()
    while queue_a:
        point, steps = queue_a.popleft()
        if steps < n_steps_a:
            for neighbor in grid.neighbors(point):
                if (neighbor not in final_spots_a) and (neighbor not in visited_a):
                    queue_a.append((neighbor, steps + 1))
                    if steps % 2 == 0:
                        visited_a.add(neighbor)
                    else:
                        final_spots_a.add(neighbor)

    return len(final_spots_a), 0


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    spots_after_64, spots_after_26501365 = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{spots_after_64=}, {spots_after_26501365=} ({time_us}ms)")
