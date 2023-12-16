import sys
from copy import deepcopy
from time import perf_counter

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
    start: Point,
    direction: Point,
    visited: set | None = None,
    visited_with_dir: set | None = None,
    cache: dict[tuple[Point, Point], set[Point]] = {},
) -> set[Point]:
    try:
        return cache[(start, direction)]
    except KeyError:
        pass
    if visited is None:
        visited = set()
    if visited_with_dir is None:
        visited_with_dir = set()
    x, y = start
    dx, dy = direction
    visited_with_dir.add(((x, y), (dx, dy)))

    if (0 <= x + dx < len(grid[0])) and (0 <= y + dy < len(grid)):
        visited.add((x, y))
        directions = INTERACTIONS[grid[y][x]][(dx, dy)]
        grid_copy = deepcopy(grid)
        row = list(grid_copy[y])
        row[x] = "#"
        grid_copy[y] = "".join(row)
        # print("\n".join(grid_copy))
        for dx, dy in directions:
            # print((x, y), (dx, dy))
            # input()
            if ((x + dx, y + dy), (dx, dy)) not in visited_with_dir:
                visited = visited.union(
                    follow_beam(
                        grid, (x + dx, y + dy), (dx, dy), visited, visited_with_dir
                    )
                )

    cache[(start, direction)] = visited
    return visited


def solve(grid: list[str]) -> tuple[int, int]:
    energized_spots_a = len(follow_beam(grid, (0, 0), (1, 0)))
    energized_spots_list = []
    width = len(grid[0])
    height = len(grid)
    for i in range(width):
        # top going south
        energized_spots_list.append(len(follow_beam(grid, (i, 0), (0, 1))))
        # bottom going north
        energized_spots_list.append(len(follow_beam(grid, (i, height - 1), (0, -1))))
    for i in range(height):
        # left going east
        energized_spots_list.append(len(follow_beam(grid, (0, i), (1, 0))))
        # right going west
        energized_spots_list.append(len(follow_beam(grid, (width - 1, i), (-1, 0))))
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
