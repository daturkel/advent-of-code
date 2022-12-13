#!/usr/bin/env python3

from functools import cmp_to_key
import sys
from time import perf_counter

Signal = list[list | int]


def parse_input(lines: list[list[str]]) -> list[list[Signal]]:
    signals = []
    for left, right in lines:
        signals.append([eval(left), eval(right)])

    return signals


def compare(left: list, right: list) -> bool | None:
    this_comparison: bool | None = None

    for i in range(len(left)):
        # if right list ran out, they're out of order
        if i >= len(right):
            return False
        match left[i], right[i]:
            case [int(), int()]:
                # do int comparisons
                if left[i] != right[i]:
                    this_comparison = left[i] < right[i]
                else:
                    this_comparison = None
            case [int(), list()]:
                this_comparison = compare([left[i]], right[i])
            case [list(), int()]:
                this_comparison = compare(left[i], [right[i]])
            case [list(), list()]:
                this_comparison = compare(left[i], right[i])

        # if a comparison was not a tie, return it
        if this_comparison is not None:
            return this_comparison

    # if left runs out
    if len(left) < len(right):
        return True
    # otherwise, tie
    else:
        return None


def get_index_sum(isgnals: list[list[Signal]]) -> int:
    idx_sum = 0
    for index, (left, right) in enumerate(signals):
        if compare(left, right):
            idx_sum += index + 1

    return idx_sum


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = [chunk.rstrip().split("\n") for chunk in file.read().split("\n\n")]

    tic = perf_counter()

    signals = parse_input(lines)
    index_sum = get_index_sum(signals)

    # chain together the pairs of signals, including [[2]] and [[6]] signals
    signals_unpaired: list[list] = sum(signals, [[[2]], [[6]]])
    # cmp_to_key lets us do bubblesort using a comparison function of our choice
    signals_sorted = sorted(
        signals_unpaired, key=cmp_to_key(lambda x, y: -1 if compare(x, y) else 1)  # type: ignore
    )
    decoder_key = (signals_sorted.index([[2]]) + 1) * (signals_sorted.index([[6]]) + 1)

    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{index_sum=}, {decoder_key=} ({time_us}ms)")
