import sys
from time import perf_counter

ADJACENT = [(-1, -1), (-1, 1), (1, 1), (1, -1), (0, 1), (0, -1), (-1, 0), (1, 0)]


def solve(lines: list[str]) -> tuple[int, int]:
    y_max = len(lines) - 1
    x_max = len(lines[0]) - 1

    for i in range(y_max + 1):
        lines[i] = list(lines[i])  # type: ignore

    def is_accessible(x: int, y: int) -> int:
        num_adjacent = 0
        for dx, dy in ADJACENT:
            xx = x + dx
            yy = y + dy
            if not (0 <= xx <= x_max) or not (0 <= yy <= y_max):
                continue
            if lines[yy][xx] == "@":
                num_adjacent += 1
            if num_adjacent >= 4:
                return 0
        return 1

    def count_accessible(remove: bool = False) -> int:
        num_accessible = 0
        for y in range(y_max + 1):
            for x in range(x_max + 1):
                if lines[y][x] == "@":
                    accessible = is_accessible(x, y)
                    num_accessible += accessible
                    if accessible and remove:
                        lines[y][x] = "."  # type: ignore
        return num_accessible

    part_one = count_accessible()
    part_two = 0
    while True:
        newly_accessible = count_accessible(remove=True)
        if newly_accessible == 0:
            break
        part_two += newly_accessible

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
