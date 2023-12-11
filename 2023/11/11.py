import sys
from itertools import combinations
from time import perf_counter


def solve(lines: list[str]) -> tuple[int, int]:
    height = len(lines[0])
    width = len(lines)
    col_map = {col: col for col in range(width)}
    row_map = {row: row for row in range(height)}
    empty_columns = {col for col in range(width)}
    empty_rows = {row for row in range(height)}
    # --------------------------------- find galaxies -------------------------------- #
    galaxies = []
    for y in range(height):
        for x in range(width):
            if lines[y][x] == "#":
                galaxies.append((x, y))
                if x in empty_columns:
                    empty_columns.difference_update([x])
                if y in empty_rows:
                    empty_rows.difference_update([y])
    # -------------------------------- adjust galaxies ------------------------------- #
    for empty_col in empty_columns:
        for col in range(empty_col, width):
            col_map[col] += 1
    for empty_row in empty_rows:
        for row in range(empty_row, height):
            row_map[row] += 1
    galaxies = [(col_map[gx], row_map[gy]) for gx, gy in galaxies]
    # --------------------------------- get distances -------------------------------- #
    total_distance = 0
    for (xa, ya), (xb, yb) in combinations(galaxies, 2):
        dx = abs(xb - xa)
        dy = abs(yb - ya)
        total_distance += dx + dy

    return total_distance, 0


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    max_distance, num_inside = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{max_distance=}, {num_inside=} ({time_us}ms)")
