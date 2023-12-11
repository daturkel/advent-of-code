import sys
from itertools import combinations
from time import perf_counter


def solve(lines: list[str]) -> tuple[int, int]:
    height = len(lines[0])
    width = len(lines)
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
    col_map_a = {col: col for col in range(width)}
    row_map_a = {row: row for row in range(height)}
    col_map_b = {col: col for col in range(width)}
    row_map_b = {row: row for row in range(height)}
    for empty_col in empty_columns:
        for col in range(empty_col, width):
            col_map_a[col] += 1
            col_map_b[col] += 999999
    for empty_row in empty_rows:
        for row in range(empty_row, height):
            row_map_a[row] += 1
            row_map_b[row] += 999999
    # --------------------------------- get distances -------------------------------- #
    total_distance_a = 0
    total_distance_b = 0
    for (xa, ya), (xb, yb) in combinations(galaxies, 2):
        dx_a = abs(col_map_a[xb] - col_map_a[xa])
        dy_a = abs(row_map_a[yb] - row_map_a[ya])
        total_distance_a += dx_a + dy_a
        dx_b = abs(col_map_b[xb] - col_map_b[xa])
        dy_b = abs(row_map_b[yb] - row_map_b[ya])
        total_distance_b += dx_b + dy_b

    return total_distance_a, total_distance_b


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    max_distance, num_inside = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{max_distance=}, {num_inside=} ({time_us}ms)")
