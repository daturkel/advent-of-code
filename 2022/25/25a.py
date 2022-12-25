#!/usr/bin/env python3

import sys
from time import perf_counter

DIGIT_MAP = {0: "0", 1: "1", 2: "2", 3: "=", 4: "-", 5: "0"}


def snafu_to_decimal(s: str) -> int:
    total = 0

    for exp, char in enumerate(reversed(s)):
        place = 5**exp
        if char in "012":
            total += place * int(char)
        elif char == "-":
            total -= place
        else:
            total -= place * 2

    return total


def decimal_to_snafu(d: int) -> str:
    reversed_digits = []
    # numbers are always >0 so don't need to handle 0 or negatives
    # first convert to base 5, via https://stackoverflow.com/a/28666223
    while d:
        reversed_digits.append(d % 5)
        d //= 5

    reversed_digits += [0]

    idx = 0
    while True:
        this_digit = reversed_digits[idx]
        if this_digit > 2:
            reversed_digits[idx + 1] += 1
        reversed_digits[idx] = DIGIT_MAP[this_digit]
        idx += 1
        if idx == len(reversed_digits) - 1:
            break

    if reversed_digits[-1] == 0:
        reversed_digits = reversed_digits[:-1]
    else:
        reversed_digits[-1] = DIGIT_MAP[reversed_digits[-1]]

    return "".join(reversed(reversed_digits))


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = [line.rstrip() for line in file.readlines()]

    tic = perf_counter()
    total = 0
    for line in lines:
        total += snafu_to_decimal(line)

    total_snafu = decimal_to_snafu(total)

    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{total_snafu=} ({time_us}ms)")
