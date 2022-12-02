#!/usr/bin/env python3

import sys
from time import perf_counter


def work(lines):
    pass


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = file.readlines()

    tic = perf_counter()
    result = work(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{result=} ({time_us}µs)")
