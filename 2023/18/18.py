import sys
from time import perf_counter

DIRECTIONS = {"R": (1, 0), "L": (-1, 0), "D": (0, 1), "U": (0, -1)}
HEX_TO_DIRECTION = {"0": "R", "1": "D", "2": "L", "3": "U"}


def get_len_border_and_area(instructions: list[tuple[str, int]]) -> tuple[int, int]:
    len_border = 1
    x, y = 0, 0
    old_x, old_y = 0, 0
    n_lines = len(instructions)
    area = 1
    for i in range(n_lines):
        direction, amount = instructions[i]
        dx, dy = DIRECTIONS[direction]
        amount = int(amount)
        len_border += amount
        old_x = x
        old_y = y
        x = x + dx * amount
        y = y + dy * amount
        # who knew! https://en.wikipedia.org/wiki/Shoelace_formula#Trapezoid_formula
        area += (old_y + y) * (old_x - x)

    # len_border - 1 to remove duplicate first point
    return len_border - 1, int(area / 2)


def get_volume(area: int, num_boundary: int) -> int:
    # Really helpful! https://en.wikipedia.org/wiki/Pick%27s_theorem
    num_interior = int(area + 1 - num_boundary / 2)
    return num_boundary + num_interior


def solve(lines: list[str]) -> tuple[int, int]:
    instructions_a = [(line.split()[0], int(line.split()[1])) for line in lines]
    len_border_a, area_a = get_len_border_and_area(instructions_a)
    volume_a = get_volume(area_a, len_border_a)

    instructions_b = []
    for line in lines:
        hex_part = line.split("#")[1]
        amount = int(hex_part[:-2], 16)
        direction = HEX_TO_DIRECTION[hex_part[-2]]
        instructions_b.append((direction, amount))
    len_border_b, area_b = get_len_border_and_area(instructions_b)
    volume_b = get_volume(area_b, len_border_b)

    return volume_a, volume_b


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    volume_a, volume_b = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{volume_a=}, {volume_b=} ({time_us}µs)")
