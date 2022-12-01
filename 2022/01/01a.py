#!/usr/bin/env python3

import logging
import sys
from time import perf_counter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[logging.StreamHandler()],
    datefmt="%H:%M:%S",
)


def get_most_calories(lines: list[str]) -> int:
    most_calories = 0
    current_calories = 0
    lines.append("\n")

    for line in lines:
        if line == "\n":
            if most_calories < current_calories:
                most_calories = current_calories
            current_calories = 0
        else:
            current_calories += int(line)

    return most_calories


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.readlines()

    result = get_most_calories(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{result=} ({time_us}µs)")
