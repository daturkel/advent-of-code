#!/usr/bin/env python3

from collections import defaultdict
import sys
from time import perf_counter
from typing import Callable

Point = tuple[int, int]


def neighbors_fn(x_max: int, y_max: int) -> Callable[[Point], list[Point]]:
    def get_neighbors(point: Point) -> list[Point]:
        x, y = point
        neighbors = [
            (x, y - 1),
            (x, y + 1),
            (x - 1, y),
            (x + 1, y),
        ]
        valid_neighbors = [
            (x, y) for x, y in neighbors if (0 <= x < x_max) and (0 <= y < y_max)
        ]

        return valid_neighbors

    return get_neighbors


def parse_input(
    lines: list[list[str]],
) -> tuple[list[list[int]], Point, Point]:
    terrain = []
    x_max = len(lines[0])
    y_max = len(lines)
    for y, line in enumerate(lines):
        if "S" in line:
            x = line.index("S")
            start = (x, y)
            line[x] = "a"
        if "E" in line:
            x = line.index("E")
            end = (x, y)
            line[x] = "z"

        terrain.append([ord(char) - 96 for char in line])

    return terrain, start, end


def find_path(terrain: list[list[int]], start: Point, end: Point | None) -> float:
    x_max = len(terrain[0])
    y_max = len(terrain)
    get_neighbors = neighbors_fn(x_max, y_max)

    distances: defaultdict[Point, float] = defaultdict(lambda: float("inf"))
    distances[start] = 0

    visited = set()

    current = start
    current_height = terrain[start[1]][start[0]]

    if end is None:
        check_done = lambda point: terrain[point[1]][point[0]] == 1
        can_move = lambda h1, h2: h1 <= h2 + 1
    else:
        check_done = lambda point: point == end
        can_move = lambda h1, h2: h2 <= h1 + 1

    while not check_done(current):
        visited.add(current)
        neighbors = [
            (nx, ny)
            for nx, ny in get_neighbors(current)
            if can_move(current_height, terrain[ny][nx])
        ]
        for neighbor in neighbors:
            this_distance = 1 + distances[current]
            if this_distance < distances[neighbor]:
                distances[neighbor] = this_distance

        current = min(
            [point for point in distances if point not in visited],
            key=lambda x: distances[x],
        )
        current_height = terrain[current[1]][current[0]]

    return distances[current]


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = [list(line.rstrip()) for line in file.readlines()]

    tic = perf_counter()

    terrain, start, end = parse_input(lines)
    distance_a = find_path(terrain, start, end)
    distance_b = find_path(terrain, end, None)

    toc = perf_counter()
    time_us = round((toc - tic), 1)

    print(f"{distance_a=}, {distance_b=} ({time_us}s)")
