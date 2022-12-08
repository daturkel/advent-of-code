#!/usr/bin/env python3

import sys
from time import perf_counter


def get_score(trees: list[list[int]], x: int, y: int) -> int:
    # get all trees in each direction, in order of closest to furthest
    leftward = trees[y][x - 1 :: -1]
    rightward = trees[y][x + 1 :]
    upward = [trees[row][x] for row in range(y - 1, -1, -1)]
    downward = [trees[row][x] for row in range(y + 1, len(trees))]

    score = 1
    height = trees[y][x]

    for horizon in [leftward, rightward, upward, downward]:
        i = 0
        for tree in horizon:
            i += 1
            if tree >= height:
                break
        score *= i

    return score


def find_best_score(trees: list[list[int]]) -> int:
    height = len(trees)
    width = len(trees[0])
    best_score = 0

    # don't need to check the edges since one side is 0 visible trees
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            tree_height = trees[y][x]
            tree_score = get_score(trees, x, y)
            if tree_score > best_score:
                best_score = tree_score

    return best_score


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        trees = [[int(char) for char in line.rstrip("\n")] for line in file.readlines()]

    tic = perf_counter()

    best_score = find_best_score(trees)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{best_score=} ({time_us}ms)")
