#!/usr/bin/env python3

import sys
from time import perf_counter


Digit = tuple[int, int]

DECRYPTION_KEY = 811589153


def encrypt(numbers: list[Digit], cipher: list[Digit] | None = None) -> list[Digit]:
    if cipher is None:
        cipher = numbers.copy()

    l = len(numbers)
    for digit in numbers:
        val = digit[0]
        idx = cipher.index(digit)
        _ = cipher.pop(idx)

        new_idx = (idx + val) % (l - 1)
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
    part_a = sum(coords)

    numbers = [(DECRYPTION_KEY * val, i) for i, val in enumerate(numbers_int)]
    encrypted: list[Digit] | None = None
    for i in range(10):
        encrypted = encrypt(numbers, encrypted)
    coords = get_coords(encrypted)
    part_b = sum(coords)

    toc = perf_counter()
    time_us = round((toc - tic), 1)

    print(f"{part_a=}, {part_b=} ({time_us}s)")
