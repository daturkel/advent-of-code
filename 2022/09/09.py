#!/usr/bin/env python3

import sys
from time import perf_counter

DIR_MAP = {"L": (-1, 0), "R": (1, 0), "U": (0, 1), "D": (0, -1)}


def follow(head: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]
    x = tail[0]
    y = tail[1]

    # don't need to move if we're already close
    if abs(dx) <= 1 and abs(dy) <= 1:
        pass
    # if we're not close but in the right column/row...
    else:
        dx = dx if dx == 0 else dx // abs(dx)
        dy = dy if dy == 0 else dy // abs(dy)
        x += dx
        y += dy
    return (x, y)


def get_visited(directions: list[list[str]]) -> tuple[int, int]:
    knots = [(0, 0) for i in range(10)]
    visited_a = [(0, 0)]
    visited_b = [(0, 0)]

    for direction, distance in directions:
        dx, dy = DIR_MAP[direction]
        for i in range(int(distance)):
            head_x = knots[0][0] + dx
            head_y = knots[0][1] + dy
            knots[0] = (head_x, head_y)
            for t in range(1, 10):
                knots[t] = follow(knots[t - 1], knots[t])

            # part a: first tail
            visited_a.append(knots[1])

            # part b: last tail
            visited_b.append(knots[-1])

    # dedupe with set (turns out this is much faster than checking to see if we'd already
    # visited a spot before appending it to the list)
    return len(set(visited_a)), len(set(visited_b))


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        directions = [line.rstrip().split(" ") for line in file.readlines()]

    tic = perf_counter()

    num_visited_a, num_visited_b = get_visited(directions)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{num_visited_a=}, {num_visited_b=} ({time_us}ms)")
