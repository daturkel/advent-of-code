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

# How many points is each choice worth
POINT_MAP = {"A": 1, "B": 2, "C": 3}
# Convenience mapping of ABC to 123 via the .index method
ABC = ["A", "B", "C"]
# Starting at the opponent's choice from ABC, do we move back
# one choice, stay where we are, or move forward one
OUTCOME_MAP = {"X": -1, "Y": 0, "Z": 1}


def get_points(games: list[str]) -> int:
    total = 0
    for game in games:
        them, outcome = game
        them = ABC.index(them)
        outcome = OUTCOME_MAP[outcome]
        me = ABC[(them + outcome) % 3]
        total += POINT_MAP[me] + 3 + 3 * outcome

    return total


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        games = [line.strip().split(" ") for line in file.readlines()]

    tic = perf_counter()
    result = get_points(games)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{result=} ({time_us}µs)")
