import sys
from time import perf_counter

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


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
    visited = set()
    # guard starts facing up
    dir_index = 0
    dx, dy = DIRS[dir_index]
    while True:
        visited.add((x, y))
        next_x, next_y = x + dx, y + dy
        if not (0 <= next_x < xmax and 0 <= next_y < ymax):
            break
        elif lines[next_y][next_x] == "#":
            dir_index = (dir_index + 1) % 4
            dx, dy = DIRS[dir_index]
        else:
            x, y = next_x, next_y

    return len(visited), 0


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
