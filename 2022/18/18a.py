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


def parse_input(lines: list[str]) -> int:
    points: set[Point] = set()
    neighbors: set[Point] = set()
    surface_area_a = 0
    for line in lines:
        point = tuple(int(char) for char in line.split(","))
        points.add(point)

    for point in points:
        for neighbor in get_neighbors(point):
            neighbors.add(neighbor)
            if neighbor not in points:
                surface_area_a += 1

    surface_area_b = surface_area_a

    for neighbor in neighbors:
        to_explore = get_neighbors(neighbor)
        explored = set()
        outside = False
        while to_explore:
            point = to_explore.pop()
            explored.add(point)
            
    return surface_area_a


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = [line.rstrip() for line in file.readlines()]

    tic = perf_counter()
    surface_area = parse_input(lines)

    toc = perf_counter()
    time_us = round((toc - tic), 1)

    print(f"{surface_area=} ({time_us}s)")
