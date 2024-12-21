import sys
from time import perf_counter


def solve(lines: list[str], save_threshold: int) -> tuple[int, int]:
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
    # populate the grid
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
    ordered_positions = []
    part_one = 0
    for (x, y), i in positions.items():
        ordered_positions.append((x, y))
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
                if saved >= save_threshold:
                    part_one += 1

    part_two = 0
    for i, (x1, y1) in enumerate(ordered_positions):
        for j, (x2, y2) in enumerate(ordered_positions[i + 1 :], start=i + 1):
            delta = j - i
            used = abs(x2 - x1) + abs(y2 - y1)
            saved = delta - used
            if saved >= save_threshold and used <= 20:
                part_two += 1

    return part_one, part_two


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    if input_file == "./test.txt":
        save_threshold = 50
    else:
        save_threshold = 100
    part_one, part_two = solve(lines, save_threshold)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
