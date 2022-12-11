#!/usr/bin/env python3

import sys
from time import perf_counter


def get_top_calories(lines: list[str]) -> tuple[int, int]:
    calories_each = []
    current_calories = 0
    lines.append("\n")

    for line in lines:
        if line == "\n":
            calories_each.append(current_calories)
            current_calories = 0
        else:
            current_calories += int(line)

    calories_each = sorted(calories_each)
    top_cals = calories_each[-1]
    top_3_cals = sum(calories_each[-3:])
    return top_cals, top_3_cals


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.readlines()

    top_cals, top_3_cals = get_top_calories(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{top_cals=}, {top_3_cals=} ({time_us}µs)")
