import sys
from collections import defaultdict
from time import perf_counter
from typing import DefaultDict

Point = tuple[int, int]

NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)

INTERACTIONS: dict[str, dict[Point, list[Point]]] = {
    "-": {EAST: [EAST], WEST: [WEST], NORTH: [EAST, WEST], SOUTH: [EAST, WEST]},
    "|": {NORTH: [NORTH], SOUTH: [SOUTH], EAST: [NORTH, SOUTH], WEST: [NORTH, SOUTH]},
    "/": {EAST: [NORTH], WEST: [SOUTH], NORTH: [EAST], SOUTH: [WEST]},
    "\\": {EAST: [SOUTH], WEST: [NORTH], NORTH: [WEST], SOUTH: [EAST]},
    ".": {EAST: [EAST], SOUTH: [SOUTH], WEST: [WEST], NORTH: [NORTH]},
}


def follow_beam(
    grid: list[str],
    width: int,
    height: int,
    start: Point,
    direction: Point,
    cache: DefaultDict[Point, list] | None = None,
) -> int | None:
    calculate_length = False
    if cache is None:
        cache = defaultdict(list)
        calculate_length = True
    x, y = start
    dx, dy = direction
    while (0 <= x < width) and (0 <= y < height):
        cache[(x, y)].append((dx, dy))
        directions = INTERACTIONS[grid[y][x]][(dx, dy)]
        try:
            dxa, dya = directions[0]
            dxb, dyb = directions[1]
            start_a = (x + dxa, y + dya)
            start_b = (x + dxb, y + dyb)
            if start_a not in cache or (dxa, dya) not in cache[start_a]:
                _ = follow_beam(grid, width, height, start_a, directions[0], cache)
            if start_b not in cache or (dxb, dyb) not in cache[start_b]:
                _ = follow_beam(grid, width, height, start_b, directions[1], cache)
            break
        except IndexError:
            dx, dy = directions[0]
            x += dx
            y += dy

    # no need to run len on any but the outermost call
    if calculate_length:
        return len(cache)


def solve(grid: list[str]) -> tuple[int, int]:
    width = len(grid[0])
    height = len(grid)
    energized_spots_a = follow_beam(grid, width, height, (0, 0), (1, 0))
    energized_spots_list = []
    for i in range(width):
        # top going south
        energized_spots_list.append(follow_beam(grid, width, height, (i, 0), (0, 1)))
        # bottom going north
        energized_spots_list.append(
            follow_beam(grid, width, height, (i, height - 1), (0, -1))
        )
    for i in range(height):
        # left going east
        energized_spots_list.append(follow_beam(grid, width, height, (0, i), (1, 0)))
        # right going west
        energized_spots_list.append(
            follow_beam(grid, width, height, (width - 1, i), (-1, 0))
        )
    return energized_spots_a, max(energized_spots_list)


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    energized_tiles, new_ways_to_win = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{energized_tiles=}, {new_ways_to_win=} ({time_us}ms)")
