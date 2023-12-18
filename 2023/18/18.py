import sys
from time import perf_counter

DIRECTIONS = {"R": (1, 0), "L": (-1, 0), "D": (0, 1), "U": (0, -1)}
POINT_TYPE: dict[tuple[str, str], str] = {
    ("D", "R"): "L",
    ("D", "L"): "J",
    ("U", "R"): "F",
    ("U", "L"): "7",
    ("R", "D"): "7",
    ("R", "U"): "J",
    ("L", "D"): "F",
    ("L", "U"): "L",
}
BORDER_CROSSINGS = {
    ("L", "7"),
    ("7", "L"),
    ("|", "|"),
    ("-", "-"),
    ("F", "J"),
    ("J", "F"),
}
BORDERS_GOING_EAST = {"L", "F", "-"}
HEX_TO_DIRECTION = {"0": "R", "1": "D", "2": "L", "3": "U"}


def get_grid(instructions: list[tuple[str, int]]) -> list[list[str]]:
    points = [(0, 0)]
    xmax = 0
    ymax = 0
    xmin = 0
    ymin = 0
    x, y = points[0]
    n_lines = len(instructions)
    point_lookup = {}
    for i in range(n_lines):
        print(i)
        last_direction = instructions[(i - 1) % n_lines][0]
        direction, amount = instructions[i]
        dx, dy = DIRECTIONS[direction]
        amount = int(amount)
        point_lookup[(x, y)] = POINT_TYPE[(last_direction, direction)]
        for i in range(1, amount + 1):
            x = x + dx
            y = y + dy
            if direction in ("L", "R"):
                point_lookup[(x, y)] = "-"
            else:
                point_lookup[(x, y)] = "|"
            xmin = min(x, xmin)
            ymin = min(y, ymin)
            xmax = max(x, xmax)
            ymax = max(y, ymax)
            points.append((x, y))
    point_lookup[(0, 0)] = POINT_TYPE[(instructions[-1][0], instructions[0][0])]

    width = xmax - xmin + 1
    height = ymax - ymin + 1

    grid = [["."] * width for _ in range(height)]
    for x, y in points:
        grid[y - ymin][x - xmin] = point_lookup.get((x, y), "#")

    return grid


def get_filled_grid_size(grid: list[list[str]]) -> int:
    total = 0
    width = len(grid[0])
    height = len(grid)
    for y in range(height):
        inside = False
        in_border = False
        border_start = ""
        border_end = ""
        for x in range(width):
            char = grid[y][x]
            if char != ".":
                total += 1
                if not in_border:
                    border_start = char
                    in_border = True
                if in_border and char not in BORDERS_GOING_EAST:
                    border_end = char
                    in_border = False
                    if (border_start, border_end) in BORDER_CROSSINGS:
                        inside = not inside
            elif inside:
                total += 1
                grid[y][x] = "*"

    return total


def solve(lines: list[str]) -> tuple[int, int]:
    instructions_a = [(line.split()[0], int(line.split()[1])) for line in lines]
    grid = get_grid(instructions_a)
    filled_grid_size = get_filled_grid_size(grid)
    # for row in grid:
    #     print("".join(row))
    instructions_b = []
    for line in lines:
        hex_part = line.split("#")[1]
        amount = int(hex_part[:-2], 16)
        direction = HEX_TO_DIRECTION[hex_part[-2]]
        instructions_b.append((direction, amount))
    grid = get_grid(instructions_b)
    print("built second grid")
    filled_grid_size = get_filled_grid_size(grid)

    return filled_grid_size, 0


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    min_heat_loss, min_heat_loss_ultra = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic), 1)

    print(f"{min_heat_loss=}, {min_heat_loss_ultra=} ({time_us}s)")
