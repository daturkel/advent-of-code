#!/usr/bin/env python3

import sys
from time import perf_counter


def parse_signals(instructions: list[list[str]]) -> tuple[int, list[list[str]]]:
    cc = 0  # cycle counter
    ic = 0  # instruction counter
    xr = 1  # x register
    hold = False  # whether or not to execute the last addx instruction yet
    amt = 0  # amount to add from last addx instruction

    strength = 0  # part a
    screen: list[list[str]] = [[] for i in range(6)]  # part b

    while ic < len(instructions):
        px = cc % 40  # pixel x coord
        py = cc // 40  # pixel y coord

        # if sprite touches x coord
        if abs(xr - px) <= 1:
            screen[py].append("#")
        else:
            screen[py].append(".")

        cc += 1  # increment cycle count

        # add strength for part a if cycle count is 20, 60, ...
        if (cc - 20) % 40 == 0:
            strength += cc * xr

        # if we were waiting on an addx instruction...
        if hold:
            ic += 1  # increment instruction counter
            xr += amt  # set x register
            hold = False  # turn off hold, we're done with this addx
        # if we get a noop
        elif instructions[ic][0] == "noop":
            ic += 1  # increment instruction counter
            continue
        # if we're receiving a new addx instruction
        else:
            # *don't* increment instruction counter
            amt = int(instructions[ic][1])  # record amt
            hold = True  # turn on hold for next cycle

    return strength, screen


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        instructions = [line.rstrip().split(" ") for line in file.readlines()]

    tic = perf_counter()

    signal_strength, screen = parse_signals(instructions)
    for line in screen:
        print("".join(line))

    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{signal_strength=} ({time_us}µs)")
