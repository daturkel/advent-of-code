#!/usr/bin/env python3

import re
import sys
from time import perf_counter

NAME_TO_VALUE = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def calibrate(lines: list[str]) -> tuple[int, int]:
    values_one = []
    values_two = []
    pattern_one = re.compile(r"\d")
    # this is a lookahead which handles overlaps like eightwo -> ["eight", "two"]:
    # (?=\d|one|two|three|...)
    pattern_two = re.compile(r"(?=(\d|" + "|".join(NAME_TO_VALUE.keys()) + "))")
    for line in lines:
        digits_one = pattern_one.findall(line)
        if digits_one:
            first, last = int(digits_one[0]), int(digits_one[-1])
        else:
            first = last = 0
        values_one.append(first * 10 + last)

        digits_two = pattern_two.findall(line)
        first, last = digits_two[0], digits_two[-1]
        first = NAME_TO_VALUE.get(first, first)
        last = NAME_TO_VALUE.get(last, last)
        values_two.append(int(first) * 10 + int(last))
    return sum(values_one), sum(values_two)


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.readlines()

    calibration_one, calibration_two = calibrate(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{calibration_one=}, {calibration_two=} ({time_us}ms)")
