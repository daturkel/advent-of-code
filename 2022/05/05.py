#!/usr/bin/env python3

import string
import sys
from time import perf_counter


def execute_move(
    stacks: list[list[str]], num: int, start: int, end: int, reverse: bool
) -> list[list[str]]:
    top, bottom = stacks[start][:num], stacks[start][num:]
    stacks[start] = bottom
    reverser = -1 if reverse else 1
    stacks[end] = top[::reverser] + stacks[end]

    return stacks


def move_boxes(lines: list[str]) -> str:
    # parse the stacks
    n_stacks = (len(lines[0]) + 1) // 4

    stacks_a = [list() for i in range(n_stacks + 1)]
    stacks_b = [list() for i in range(n_stacks + 1)]

    for line_no, line in enumerate(lines):
        if line == "":
            break
        for i, char in enumerate(line):
            if char == "[":
                stacks_a[(i // 4)].append(line[i + 1])
                stacks_b[(i // 4)].append(line[i + 1])

    # parse the instructions
    for line in lines[line_no + 1 :]:
        words = line.split(" ")
        num = int(words[1])
        start = int(words[3]) - 1
        end = int(words[5]) - 1

        stacks_a = execute_move(stacks_a, num, start, end, reverse=True)
        stacks_b = execute_move(stacks_b, num, start, end, reverse=False)

    # get the top of each stack
    return_str_a = ""
    return_str_b = ""
    for i in range(n_stacks):
        if stacks_a[i]:
            return_str_a += stacks_a[i][0]
        if stacks_b[i]:
            return_str_b += stacks_b[i][0]
    return return_str_a, return_str_b


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = [line.rstrip("\n") for line in file.readlines()]

    tic = perf_counter()

    str_a, str_b = move_boxes(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{str_a=}, {str_b=} {time_us}µs)")
