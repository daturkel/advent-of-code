#!/usr/bin/env python3

import sys
from time import perf_counter


def find_overlaps(lines: list[list[str]]) -> tuple[int, int]:
    total_a = 0
    total_b = 0
    for l, r in lines:
        lmin, lmax = [int(num) for num in l.split("-")]
        rmin, rmax = [int(num) for num in r.split("-")]
        if (lmin <= rmin and lmax >= rmax) or (rmin <= lmin and rmax >= lmax):
            total_a += 1
        if (lmin <= rmin and lmax >= rmin) or (rmin <= lmin and rmax >= lmin):
            total_b += 1

    return total_a, total_b


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = [line.strip().split(",") for line in file.readlines()]

    tic = perf_counter()
    result_a, result_b = find_overlaps(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{result_a=}, {result_b=} ({time_us}µs)")
