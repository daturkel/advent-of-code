import sys
from time import perf_counter

DIR_TO_DELTA = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}


def can_shift(grid: list[list[str]], x: int, y: int, dx: int, dy: int) -> bool:
    next_char = grid[y + dy][x + dx]
    if next_char == ".":
        return True
    elif next_char == "O":
        return can_shift(grid, x + dx, y + dy, dx, dy)
    elif next_char == "[":
        return can_shift(grid, x + dx, y + dy, dx, dy) and can_shift(
            grid, x + dx + 1, y + dy, dx, dy
        )
    elif next_char == "]":
        return can_shift(grid, x + dx, y + dy, dx, dy) and can_shift(
            grid, x + dx + 1, y + dy, dx, dy
        )
    else:
        return False


def shift(grid: list[list[str]], x: int, y: int, dx: int, dy: int):
    next_char = grid[y + dy][x + dx]
    if next_char == ".":
        grid[y + dy][x + dx] = grid[y][x]
        grid[y][x] = "."
    elif next_char == "O":
        shift(grid, x + dx, y + dy, dx, dy)
        grid[y + dy][x + dx] = grid[y][x]
        grid[y][x] = "."
    elif next_char == "[":
        shift(grid, x + dx, y + dy, dx, dy)
        shift(grid, x + 1 + dx, y + dy, dx, dy)
    elif next_char == "]":
        if can_shift(grid, x + dx, y + dy, dx, dy):
            shift(grid, x + dx, y + dy, dx, dy)
            shift(grid, x - 1 + dx, y + dy, dx, dy)


def simulate(
    x0: int,
    y0: int,
    grid: list[list[str]],
    directions: list[tuple[int, int]],
    debug: bool = False,
):
    x, y = x0, y0
    for dx, dy in directions:
        if can_shift(grid, x, y, dx, dy):
            shift(grid, x, y, dx, dy)
            x += dx
            y += dy
        if debug:
            print(dx, dy)
            show(grid)
            input()
    return grid


def get_gps(grid: list[list["str"]]) -> int:
    gps = 0
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char in ("O", "["):
                gps += x + 100 * y
    return gps


def show(grid: list[list[str]]):
    for row in grid:
        print("".join(row))
    print("\n--------\n")


def solve(lines: list[str]) -> tuple[int, int]:
    # parse inputs
    grid = []
    x0, y0 = 0, 0
    for y, line in enumerate(lines):
        if line == "":
            break
        row = []
        for x, char in enumerate(line):
            row.append(char)
            if char == "@":
                x0, y0 = (x, y)
        grid.append(list(line))

    # make part 2 grid
    new_grid = []
    for line in grid:
        row = []
        for char in line:
            if char == "#":
                row += ["#", "#"]
            elif char == "O":
                row += ["[", "]"]
            elif char == ".":
                row += [".", "."]
            else:
                row += ["@", "."]
        new_grid.append(row)

    directions = []
    for line in lines[y + 1 :]:
        directions += [DIR_TO_DELTA[d] for d in line]

    # simulate robot
    grid = simulate(x0, y0, grid, directions)

    # calculate score
    gps_one = get_gps(grid)

    # part two
    # show(new_grid)

    gps_two = 0
    # new_grid = simulate(x0 * 2, y0, new_grid, directions)
    # show(new_grid)
    # gps_two = get_gps(new_grid)

    return gps_one, gps_two


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
