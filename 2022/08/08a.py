#!/usr/bin/env python3

import sys
from time import perf_counter


def count_visible(trees: list[list[int]]) -> int:
    height = len(trees)
    width = len(trees[0])
    # the edge is always visible
    num_visible = 2 * (width) + 2 * (height - 2)
    visible_indices = []

    # horizontal visibility
    for y in range(1, height - 1):
        max_left = trees[y][0]
        max_right = trees[y][width - 1]
        for x in range(1, width - 1):
            tree_left = trees[y][x]
            tree_right = trees[y][width - x - 1]
            if tree_left > max_left:
                max_left = tree_left
                visible_indices.append((x, y))
            if tree_right > max_right:
                max_right = tree_right
                visible_indices.append((width - x - 1, y))

    # vertical visibility
    for x in range(1, width - 1):
        max_up = trees[0][x]
        max_down = trees[height - 1][x]
        for y in range(1, height - 1):
            tree_up = trees[y][x]
            tree_down = trees[height - y - 1][x]
            if tree_up > max_up:
                max_up = tree_up
                visible_indices.append((x, y))
            if tree_down > max_down:
                max_down = tree_down
                visible_indices.append((x, height - y - 1))

    # set() to dedupe
    num_visible += len(set(visible_indices))

    return num_visible


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        trees = [[int(char) for char in line.rstrip("\n")] for line in file.readlines()]

    tic = perf_counter()

    num_visible = count_visible(trees)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{num_visible=} ({time_us}µs)")
