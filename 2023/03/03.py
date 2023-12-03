import re
import sys
from collections import defaultdict
from time import perf_counter

NON_SYMBOL_CHARS = set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."])


def get_char_type(char: str) -> int:
    if char == "*":
        return 2
    elif char not in NON_SYMBOL_CHARS:
        return 1
    return 0


def get_indices_around(
    x_start: int, x_end: int, y: int, max_x: int, max_y: int
) -> list[tuple[int, int]]:
    indices = []
    for x in range(x_start - 1, x_end + 1):
        if 0 <= x < max_x:
            if y + 1 < max_y:  # indices below
                indices.append((x, y + 1))
            if y - 1 >= 0:  # indices above
                indices.append((x, y - 1))
    if x_start - 1 >= 0:  # index to the left
        indices.append((x_start - 1, y))
    if x_end < max_x:  # index to the right
        indices.append((x_end, y))
    return indices


def add_parts(lines: list[str]) -> tuple[int, int]:
    pattern = re.compile(r"\d+")
    parts_total = 0
    max_y = len(lines)
    max_x = len(lines[0])
    possible_gears = defaultdict(list)
    for y, line in enumerate(lines):
        matches = pattern.finditer(line)  # find numbers on line
        for match in matches:
            x_start, x_end = match.span()
            part_number = int(match.group(0))
            # find every point around the number
            indices_to_check = get_indices_around(x_start, x_end, y, max_x, max_y)
            valid_part = False
            # check if each index is punctuation
            for xi, yi in indices_to_check:
                is_special = get_char_type(lines[yi][xi])
                if is_special:
                    if not valid_part:
                        parts_total += part_number
                        valid_part = True

                    if is_special == 2:
                        # build up dictionary of asterisk location to list of parts
                        possible_gears[(xi, yi)].append(part_number)

    gear_total = 0
    for _, parts in possible_gears.items():
        # sum up gear products
        if len(parts) == 2:
            gear_total += parts[0] * parts[1]

    return parts_total, gear_total


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    parts_total, gear_total = add_parts(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{parts_total=}, {gear_total=} ({time_us}µs)")
