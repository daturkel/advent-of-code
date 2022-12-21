#!/usr/bin/env python3

from operator import add, mul, sub, floordiv as div
import sys
from time import perf_counter

OP_DICT = {"+": add, "*": mul, "-": sub, "/": div}


def parse_input(lines: list[list[str]]) -> int:
    numbers = {}
    next_lines = []

    while True:
        for line in lines:
            name = line[0][:-1]
            if len(line) == 2:
                numbers[name] = int(line[1])
                continue

            try:
                l_str, op_str, r_str = line[1:]
                op = OP_DICT[op_str]
                l = numbers[l_str]
                r = numbers[r_str]
                numbers[name] = op(l, r)
            except KeyError:
                next_lines.append(line)

        if "root" in numbers:
            break
        lines = next_lines.copy()
        next_lines = []

    return numbers["root"]


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = [line.split() for line in file.readlines()]

    tic = perf_counter()
    result = parse_input(lines)

    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{result=} ({time_us}ms)")
