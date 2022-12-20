#!/usr/bin/env python3

from dataclasses import dataclass
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


def is_outside(
    point: Point,
    known_inside: set[Point],
    known_outside: set[Point],
    skip: set[Point] | None = None,
):
    unknown = []
    if skip is None:
        skip = set()

    for neighbor in get_neighbors(point):
        if neighbor in skip:
            continue

        if neighbor in known_outside:
            return True, known_inside, known_outside
        elif neighbor in known_inside:
            continue
        else:
            unknown.append(neighbor)

    while unknown:
        this_point = unknown.pop()
        outside, known_inside, known_outside = is_outside(
            this_point, known_inside, known_outside, skip.add(point)
        )
        if outside:
            known_outside.add(this_point)
            return True, known_inside, known_outside
        elif outside is False:
            known_inside.add(this_point)
        else:
            unknown.append(this_point)

    return False, known_inside, known_outside


def parse_input(lines: list[str]) -> int:
    points: set[Point] = set()
    neighbors: set[Point] = set()
    surface_area_a = 0
    surface_area_b = 0
    for line in lines:
        point = tuple(int(char) for char in line.split(","))
        points.add(point)

    for point in points:
        for neighbor in get_neighbors(point):
            neighbors.add(neighbor)
            if neighbor not in points:
                surface_area_a += 1

    # not the most efficient way to do this
    known_inside = set([pt for pt in points])
    known_outside = set()
    for point in points:
        for neighbor in get_neighbors(point):
            outside, known_inside, known_outside = is_outside(
                neighbor, known_inside, known_outside
            )
            if outside:
                surface_area_b += 1

    return surface_area_a, surface_area_b


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = [line.rstrip() for line in file.readlines()]

    tic = perf_counter()
    surface_area = parse_input(lines)

    toc = perf_counter()
    time_us = round((toc - tic), 1)

    print(f"{surface_area=} ({time_us}s)")
