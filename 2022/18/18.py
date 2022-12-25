#!/usr/bin/env python3


from collections import deque
import sys
from time import perf_counter

Point = tuple[int, ...]


def get_neighbors(point: Point) -> list[Point]:
    x, y, z = point
    return [
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    ]


def parse_input(lines: list[str]) -> tuple[int, int]:
    points: set[Point] = set()
    surface_area_a = 0
    surface_area_b = 0

    min_x = 100
    min_y = 100
    min_z = 100
    max_x = 0
    max_y = 0
    max_z = 0

    for line in lines:
        point = tuple(int(char) for char in line.split(","))
        points.add(point)

        x, y, z = point

        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
        min_z = min(min_z, z)
        max_z = max(max_z, z)

    # routine for getting outside points stolen from ephemient's solution
    # https://github.com/ephemient/aoc2022/blob/main/py/aoc2022/day18.py
    outside: set[Point] = set()
    queue: deque[Point] = deque()
    start = (min_x - 1, min_y - 1, min_z - 1)
    queue.append(start)
    outside.add(start)
    while queue:
        point = queue.popleft()
        for nx, ny, nz in get_neighbors(point):
            if (
                (min_x - 1 <= nx <= max_x + 1)
                and (min_y - 1 <= ny <= max_y + 1)
                and (min_z - 1 <= nz <= max_z + 1)
                and (nx, ny, nz) not in points
                and (nx, ny, nz) not in outside
            ):
                queue.append((nx, ny, nz))
                outside.add((nx, ny, nz))

    for point in points:
        for neighbor in get_neighbors(point):
            if neighbor not in points:
                surface_area_a += 1
                if neighbor in outside:
                    surface_area_b += 1

    return surface_area_a, surface_area_b


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = [line.rstrip() for line in file.readlines()]

    tic = perf_counter()
    surface_area = parse_input(lines)

    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{surface_area=} ({time_us}ms)")
