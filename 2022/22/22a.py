#!/usr/bin/env python3

import re
import sys
from time import perf_counter
from typing import Literal

Point = tuple[int, int]

BEARINGS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


class Board:
    def __init__(self, lines: list[str]):
        self.grid = []

        # add 2 to max width and height because we're going to pad sides with a space
        self.width = max(len(line) for line in lines) + 2
        self.height = len(lines) + 2
        self.grid.append([" "] * self.width)
        for line in lines:
            line = line.rstrip()
            line_width = len(line)
            line = " " + line + " " * (self.width - line_width - 1)
            self.grid.append(list(line))
        self.grid.append([" "] * self.width)

    def show(self, point: Point | None = None):
        if point:
            x, y = point
            tmp = self.grid[y][x]
            self.grid[y][x] = "@"

        for line in self.grid:
            print("".join(line))

        if point:
            self.grid[y][x] = tmp

    def starting_point(self) -> Point:
        y = 1
        x = self.grid[y].index(".")
        return (x, y)

    def move(self, point: Point, bearing: Point) -> Point:
        nx, ny = point[0] + bearing[0], point[1] + bearing[1]

        next_point_type = self.grid[ny][nx]
        while next_point_type == " ":
            nx, ny = (nx + bearing[0]) % self.width, (ny + bearing[1]) % self.height
            next_point_type = self.grid[ny][nx]

        if next_point_type == "#":
            return point
        else:
            return (nx, ny)


def parse_directions(directions: str) -> list[Literal["R", "L"] | int]:
    direction_list = re.findall(r"(\d+|\D+)", directions)
    for i in range(len(direction_list)):
        try:
            direction_list[i] = int(direction_list[i])
        except ValueError:
            pass

    return direction_list


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        board_lines, directions = file.read().split("\n\n")

    tic = perf_counter()
    board = Board(board_lines.split("\n"))
    direction_list = parse_directions(directions.rstrip())

    bearing_idx = 0
    point = board.starting_point()

    for direction in direction_list:
        if direction == "R":
            bearing_idx = (bearing_idx + 1) % 4
            continue
        elif direction == "L":
            bearing_idx = (bearing_idx - 1) % 4
            continue

        for i in range(direction):
            bearing = BEARINGS[bearing_idx]
            next_point = board.move(point, bearing)
            # if we stopped moving, break
            if next_point == point:
                break
            # otherwise, move
            point = next_point

    x, y = point
    password = 1000 * y + 4 * x + bearing_idx
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{password=} ({time_us}ms)")
