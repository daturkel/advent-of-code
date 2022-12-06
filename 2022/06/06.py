#!/usr/bin/env python3

import sys
from time import perf_counter


def get_indices(signal: str) -> tuple[int, int]:
    idx_a = None
    idx_b = None
    i = 0
    while not (idx_a and idx_b):
        chunk_a = signal[i : i + 4]
        chunk_b = signal[i : i + 14]
        if (not idx_a) and (len(set(chunk_a)) == 4):
            idx_a = i + 4
        if (not idx_b) and (len(set(chunk_b)) == 14):
            idx_b = i + 14
        i += 1
    return idx_a, idx_b


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        signal = file.read()

    tic = perf_counter()

    start_of_packet, start_of_message = get_indices(signal)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{start_of_packet=}, {start_of_message=} {time_us}µs)")
