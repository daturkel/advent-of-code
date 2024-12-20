import sys
from collections import defaultdict
from time import perf_counter


def solve(lines: list[str]) -> tuple[int, int]:
    positions = dict()
    xmax = len(lines[0])
    ymax = len(lines)
    for y0, line in enumerate(lines):
        if "S" in line:
            x0 = line.index("S")
            break
    x, y = x0, y0
    i = 0
    positions[(x0, y0)] = i
    reached_end = False
    i += 1
    while not reached_end:
        for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if (nx, ny) in positions:
                continue
            if (0 <= nx < xmax) and (0 <= ny < ymax) and lines[ny][nx] != "#":
                x, y = nx, ny
                positions[(x, y)] = i
                i += 1
                if lines[ny][nx] == "E":
                    reached_end = True
    cheats = defaultdict(int)
    for (x, y), i in positions.items():
        start = positions[(x, y)]
        for nx, ny in [
            (x - 2, y),
            (x + 2, y),
            (x, y - 2),
            (x, y + 2),
            (x - 1, y - 1),
            (x - 1, y + 1),
            (x + 1, y - 1),
            (x + 1, y + 1),
        ]:
            if (nx, ny) in positions:
                delta = positions[(nx, ny)] - start
                saved = delta - 2
                if saved > 0:
                    cheats[saved] += 1

    part_one = sum(v for k, v in cheats.items() if k >= 100)

    return part_one, 0


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
