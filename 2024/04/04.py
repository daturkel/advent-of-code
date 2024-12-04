import sys
from time import perf_counter

DIRECTIONS = [(0, 1), (1, 0), (1, 1), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1)]


def search_xmas(puzzle: list[str], x0: int, y0: int, xmax: int, ymax: int) -> int:
    count = 0
    for dx, dy in DIRECTIONS:
        remaining = ["S", "A", "M"]  # pop pops from the right
        x, y = x0, y0
        valid = True
        while remaining:
            next_char = remaining.pop()
            x += dx
            y += dy
            if (
                not (0 <= x <= xmax)
                or not (0 <= y <= ymax)
                or puzzle[y][x] != next_char
            ):
                valid = False
                break
        if valid:
            count += 1

    return count


def search_x_mas(puzzle: list[str], x: int, y: int) -> int:
    valid_mas = {("M", "A", "S"), ("S", "A", "M")}
    if ((puzzle[y][x], puzzle[y + 1][x + 1], puzzle[y + 2][x + 2]) in valid_mas) and (
        puzzle[y + 2][x],
        puzzle[y + 1][x + 1],
        puzzle[y][x + 2],
    ) in valid_mas:
        return 1
    return 0


def solve(puzzle: list[str]) -> tuple[int, int]:
    xmas_count = 0
    x_mas_count = 0
    xmax = len(puzzle[0]) - 1
    ymax = len(puzzle) - 1
    for y, line in enumerate(puzzle):
        for x, char in enumerate(line):
            if char == "X":
                xmas_count += search_xmas(puzzle, x, y, xmax, ymax)
            elif (x <= xmax - 2) and (y <= ymax - 2) and char in {"M", "S"}:
                x_mas_count += search_x_mas(puzzle, x, y)

    return xmas_count, x_mas_count


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
