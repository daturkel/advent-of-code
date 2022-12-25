#!/usr/bin/env python3

import sys
from time import perf_counter

# An artifact of a failed attempt before I found a much better solution

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
    max_x: int,
    max_y: int,
    max_z: int,
    skip: set[Point] | None = None,
):
    unknown = []
    if skip is None:
        skip = set()

    inside_neighbors = 0
    neighbors = [neighbor for neighbor in get_neighbors(point) if neighbor not in skip]
    for neighbor in neighbors:
        if (
            (neighbor in known_outside)
            or not (0 <= neighbor[0] <= max_x)
            or not (0 <= neighbor[1] <= max_y)
            or not (0 <= neighbor[2] <= max_z)
        ):
            known_outside.add(neighbor)
            return True, known_inside, known_outside
        elif neighbor in known_inside:
            inside_neighbors += 1
            continue
        else:
            unknown.append(neighbor)

    if inside_neighbors == len(neighbors):
        return False, known_inside, known_outside

    while unknown:
        this_point = unknown.pop()
        new_skip = skip.copy()
        new_skip.add(point)
        outside, known_inside, known_outside = is_outside(
            this_point, known_inside, known_outside, max_x, max_y, max_z, new_skip
        )
        if outside:
            known_outside.add(this_point)
            return True, known_inside, known_outside
        elif outside is False:
            known_inside.add(this_point)

    return False, known_inside, known_outside


def parse_input(lines: list[str]) -> tuple[int, int]:
    points: set[Point] = set()
    neighbors: list[Point] = []
    surface_area_a = 0
    surface_area_b = 0

    max_x = 0
    max_y = 0
    max_z = 0
    for line in lines:
        point = tuple(int(char) for char in line.split(","))
        max_x = max(max_x, point[0])
        max_y = max(max_y, point[1])
        max_z = max(max_z, point[2])
        points.add(point)

    for point in points:
        for neighbor in get_neighbors(point):
            neighbors.append(neighbor)
            if neighbor not in points:
                surface_area_a += 1

    # not the most efficient way to do this
    known_inside = set([pt for pt in points])
    known_outside: set[Point] = set()
    for neighbor in neighbors:
        if neighbor in known_inside:
            continue
        elif neighbor in known_outside:
            surface_area_b += 1
        else:
            outside, known_inside, known_outside = is_outside(
                neighbor, known_inside, known_outside, max_x, max_y, max_z
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
