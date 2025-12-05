import sys
from time import perf_counter


def solve(lines: list[str]) -> tuple[int, int]:
    part_one = 0

    ranges = []
    for i, line in enumerate(lines):
        if line == "":
            break
        lo, hi = line.split("-", 1)
        lo = int(lo)
        hi = int(hi)
        ranges.append(range(lo, hi + 1))

    for line in lines[i + 1 :]:
        for range_ in ranges:
            if int(line) in range_:
                part_one += 1
                break

    part_two = 0

    return part_one, part_two


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
