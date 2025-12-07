import sys
from collections import defaultdict
from time import perf_counter


def solve(lines: list[str]) -> tuple[int, int]:
    s = lines[0].index("S")
    current_indices = [s]
    next_indices = []
    splits = set()
    paths_here = defaultdict(int)
    paths_here[(s, 0)] = 1

    for y, line in enumerate(lines[1:]):
        for x in set(current_indices):
            if line[x] == ".":
                next_indices.append(x)
                paths_here[(x, y + 1)] += paths_here[(x, y)]
            elif line[x] == "^":
                splits.add((x, y))
                next_indices += [x - 1, x + 1]
                dist = paths_here[(x, y)]
                paths_here[(x - 1, y + 1)] += dist
                paths_here[(x + 1, y + 1)] += dist
        current_indices = next_indices
        next_indices = []

    return len(splits), sum(
        v for (_, y), v in paths_here.items() if y == len(lines) - 1
    )


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{part_one=}, {part_two=} ({time_us}µs)")
