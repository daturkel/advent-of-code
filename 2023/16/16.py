import sys
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
    grid: list[str], start: Point, direction: Point, cache: set | None = None
) -> int:
    if cache is None:
        cache = set()
    width = len(grid[0])
    height = len(grid)
    x, y = start
    dx, dy = direction
    while (0 <= x < width) and (0 <= y < height):
        cache.add(((x, y), (dx, dy)))
        directions = INTERACTIONS[grid[y][x]][(dx, dy)]
        if len(directions) == 1:
            dx, dy = directions[0]
            x += dx
            y += dy
        else:
            dxa, dya = directions[0]
            dxb, dyb = directions[1]
            if ((x + dxa, y + dya), (directions[0])) not in cache:
                _ = follow_beam(grid, (x + dxa, y + dya), directions[0], cache)
            if ((x + dxb, y + dyb), (directions[1])) not in cache:
                _ = follow_beam(grid, (x + dxb, y + dyb), directions[1], cache)
            break

    num_visited = len(set([start for start, _ in cache]))
    return num_visited


def solve(grid: list[str]) -> tuple[int, int]:
    energized_spots_a = follow_beam(grid, (0, 0), (1, 0))
    energized_spots_list = []
    width = len(grid[0])
    height = len(grid)
    for i in range(width):
        # top going south
        energized_spots_list.append(follow_beam(grid, (i, 0), (0, 1)))
        # bottom going north
        energized_spots_list.append(follow_beam(grid, (i, height - 1), (0, -1)))
    for i in range(height):
        # left going east
        energized_spots_list.append(follow_beam(grid, (0, i), (1, 0)))
        # right going west
        energized_spots_list.append(follow_beam(grid, (width - 1, i), (-1, 0)))
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
