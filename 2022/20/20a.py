#!/usr/bin/env python3

import sys
from time import perf_counter


Digit = tuple[int, int]


def encrypt(numbers: list[Digit]) -> list[Digit]:
    cipher = numbers.copy()
    l = len(numbers)
    for digit in numbers:
        val = digit[0]
        idx = cipher.index(digit)
        _ = cipher.pop(idx)

        new_idx_raw = idx + val
        # handle weird wraparound stuff (new_idx_raw // l is how many times we wrap around)
        if (new_idx_raw < 0) or (new_idx_raw >= l):
            new_idx_raw += (new_idx_raw // l)

        new_idx = new_idx_raw % l
        cipher.insert(new_idx, digit)

    return cipher


def get_coords(numbers: list[Digit]) -> tuple[int, int, int]:
    l = len(numbers)
    numbers_raw = [digit[0] for digit in numbers]
    idx_0 = numbers_raw.index(0)
    return (
        numbers_raw[(idx_0 + 1000) % l],
        numbers_raw[(idx_0 + 2000) % l],
        numbers_raw[(idx_0 + 3000) % l],
    )


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        numbers_int = [int(num) for num in file.readlines()]

    tic = perf_counter()
    numbers = [(val, i) for i, val in enumerate(numbers_int)]
    encrypted = encrypt(numbers)
    coords = get_coords(encrypted)
    sum_of_coords = sum(coords)

    toc = perf_counter()
    time_us = round((toc - tic), 1)

    print(f"{sum_of_coords=} ({time_us}s)")
