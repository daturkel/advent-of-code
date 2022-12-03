#!/usr/bin/env python3

import string
import sys
from time import perf_counter


def get_priority(char: str) -> int:
    if char in string.ascii_lowercase:
        # ord("A") = 65, plus the 26 extra pts for uppercase
        offset = 96
    else:
        # ord("A") = 65, plus the 26 extra pts for uppercase
        offset = 38
    return ord(char) - offset


def sum_badges(rucksacks: list[str]) -> int:
    total = 0
    for group_idx in range(len(rucksacks) // 3):
        group = rucksacks[(group_idx * 3) : (group_idx + 1) * 3]
        badge = set.intersection(*[set(rucksack) for rucksack in group])
        badge = list(badge)[0]
        total += get_priority(badge)

    return total


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        rucksacks = [line.strip() for line in file.readlines()]

    tic = perf_counter()
    result = sum_badges(rucksacks)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{result=} ({time_us}µs)")
