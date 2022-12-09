#!/usr/bin/env python3

import sys
from time import perf_counter

# How many points is each choice worth
POINT_MAP = {"X": 1, "Y": 2, "Z": 3}
# Map a pair of choices to a win/lose
WIN_MAP = {
    "X": {"B": -1, "C": 1},
    "Y": {"A": 1, "C": -1},
    "Z": {"A": -1, "B": 1},
}


def get_points(games: list[list[str]]) -> int:
    total = 0
    for game in games:
        them, me = game
        total += POINT_MAP[me] + 3 + 3 * WIN_MAP[me].get(them, 0)

    return total


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        games = [line.strip().split(" ") for line in file.readlines()]

    tic = perf_counter()
    result = get_points(games)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{result=} ({time_us}µs)")
