#!/usr/bin/env python3

import re
import sys
from time import perf_counter

Point = tuple[int, int]


def manhattan(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x2 - x1) + abs(y2 - y1)


def get_perimeter(x: int, y: int, radius: int, max_coord: int) -> list[Point]:
    perim_radius = radius + 1
    perimeter = []

    min_y = max(y - perim_radius, 0)
    max_y = min(y + perim_radius, max_coord)

    for py in range(min_y, max_y + 1):
        distance_remaining = perim_radius - abs(y - py)

        if x + distance_remaining <= max_coord:
            perimeter.append((x + distance_remaining, py))
        if x - distance_remaining >= 0:
            perimeter.append((x - distance_remaining, py))

    return perimeter


def parse_input(lines: list[str], max_coord: int) -> Point:
    # find x=number or y=number, including negative numbers
    pattern = re.compile(r".=(-?\d+)")

    sensors = []

    # collect all the sensors and their radii
    for line in lines:
        sx, sy, bx, by = [int(s) for s in pattern.findall(line)]
        radius = manhattan(sx, sy, bx, by)
        sensors.append(((sx, sy), radius))

    # for each sensor, find its perimeter (points that are unreachable by 1)
    for (sx, sy), radius in sensors:
        perimeter = get_perimeter(sx, sy, radius, max_coord)
        # for each point on the perimeter, check if it's reachable by any sensor
        for (px, py) in perimeter:
            reachable = False
            for (sx, sy), radius in sensors:
                if manhattan(px, py, sx, sy) <= radius:
                    reachable = True
                    break

            # if we found an unreachable point, we're done
            if not reachable:
                return (px, py)

    raise ValueError("Unreachable point not found")


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = [line.rstrip() for line in file.readlines()]

    tic = perf_counter()
    max_coord = 4000000 if len(sys.argv) > 1 else 20
    bx, by = parse_input(lines, max_coord)
    frequency = 4000000 * bx + by

    toc = perf_counter()
    time_us = round((toc - tic), 1)

    print(f"{frequency=} ({time_us}s)")
