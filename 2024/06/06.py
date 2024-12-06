import sys
from collections import defaultdict
from time import perf_counter

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def get_journey_length(
    lines: list[str],
    x: int,
    y: int,
    xmax: int,
    ymax: int,
    obs_x: int | None = None,
    obs_y: int | None = None,
) -> dict[tuple[int, int], set[tuple[int, int]]]:
    visited = defaultdict(set)
    dir_index = 0
    dx, dy = DIRS[dir_index]
    while True:
        if (dx, dy) in visited[(x, y)]:
            raise RuntimeError("loop!")
        visited[(x, y)].add((dx, dy))
        next_x, next_y = x + dx, y + dy
        if not (0 <= next_x < xmax and 0 <= next_y < ymax):
            break
        elif (lines[next_y][next_x] == "#") or (next_x, next_y) == (obs_x, obs_y):
            dir_index = (dir_index + 1) % 4
            dx, dy = DIRS[dir_index]
        else:
            x, y = next_x, next_y
    return visited


def solve(lines: list[str]) -> tuple[int, int]:
    xmax = len(lines[0])
    ymax = len(lines)
    for y, line in enumerate(lines):
        try:
            # guard starts facing up in both test and real input
            x = line.index("^")
            break
        except ValueError:
            pass
    part_one_dict = get_journey_length(lines, x, y, xmax, ymax)
    part_one = len(part_one_dict)
    del part_one_dict[(x, y)]  # don't put obstacle at starting position
    loop_creators = 0
    for obs_x, obs_y in part_one_dict:
        try:
            get_journey_length(lines, x, y, xmax, ymax, obs_x, obs_y)
        except RuntimeError:
            loop_creators += 1

    return part_one, loop_creators


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
