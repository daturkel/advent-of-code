#!/usr/bin/env python3

import re
import sys
from time import perf_counter

Point = tuple[int, int]


def manhattan(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x2 - x1) + abs(y2 - y1)


def row_intersection(x: int, y: int, radius: int, row_number: int) -> list[Point]:
    intersection = []
    if manhattan(x, y, x, row_number) <= radius:
        intersection.append((x, row_number))
    l = x - 1
    r = x + 1
    while True:
        l_valid = manhattan(x, y, l, row_number) <= radius
        if l_valid:
            intersection.append((l, row_number))

        r_valid = manhattan(x, y, r, row_number) <= radius
        if r_valid:
            intersection.append((r, row_number))

        if l_valid or r_valid:
            l = l - 1
            r = r + 1
        else:
            break

    return intersection


def parse_input(lines: list[str], row_number: int) -> int:
    # find x=number or y=number, including negative numbers
    pattern = re.compile(r".=(-?\d+)")
    known_beacons = []
    row_in_radius = []

    sensors = []

    for line in lines:
        sx, sy, bx, by = [int(s) for s in pattern.findall(line)]
        radius = manhattan(sx, sy, bx, by)
        sensors.append(((sx, sy), radius))

        if by == row_number:
            known_beacons.append((bx, by))

        row_in_radius.append(row_intersection(sx, sy, radius, row_number))

    all_row_in_radius = set(sum(row_in_radius, []))

    number_non_beacons = len(all_row_in_radius.difference(known_beacons))

    return number_non_beacons


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = [line.rstrip() for line in file.readlines()]

    tic = perf_counter()
    row_number = 2000000 if len(sys.argv) > 1 else 10
    number_non_beacons = parse_input(lines, row_number)

    toc = perf_counter()
    time_us = round((toc - tic), 1)

    print(f"{number_non_beacons=} ({time_us}s)")
