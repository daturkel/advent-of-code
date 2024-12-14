import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from time import perf_counter

PATTERN = re.compile(r"[-\d]+")


@dataclass
class Robot:
    x: int
    y: int
    dx: int
    dy: int

    def move(self, times: int, xmax: int, ymax: int):
        self.x = (self.x + times * self.dx) % xmax
        self.y = (self.y + times * self.dy) % ymax


def point_to_quadrant(x: int, y: int, xmax: int, ymax: int) -> int:
    if x < xmax // 2:
        if y < ymax // 2:
            return 0
        elif y > ymax // 2:
            return 2
    elif x > xmax // 2:
        if y < ymax // 2:
            return 1
        elif y > ymax // 2:
            return 3
    return 4


def show(robots: list[Robot], xmax: int, ymax: int):
    grid = []

    for _ in range(ymax):
        grid.append([" " for _ in range(xmax)])

    for robot in robots:
        grid[robot.y][robot.x] = "X"

    for line in grid:
        print("".join(line))


def solve(lines: list[str], xmax: int, ymax: int) -> tuple[int, int]:
    robots = []
    for line in lines:
        x, y, dx, dy = PATTERN.findall(line)
        robots.append(Robot(int(x), int(y), int(dx), int(dy)))

    part_one = 0
    min_danger = (101 * 103) ** 4
    min_danger_idx = 0
    for i in range(xmax * ymax + 1):
        grid = [[" " for _ in range(xmax)] for _ in range(ymax)]
        quadrants = [0, 0, 0, 0, 0]
        for robot in robots:
            robot.move(1, xmax, ymax)
            grid[robot.y][robot.x] = "X"
            quadrant = point_to_quadrant(robot.x, robot.y, xmax, ymax)
            quadrants[quadrant] += 1
        # part one
        danger = quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]
        if i == 99:
            part_one = danger
        # part two, silly version
        for row in grid:
            if "XXXXXXXXXXXXXXX" in "".join(row):
                return part_one, i + 1
        # part two, danger minimizing version
        # if danger < min_danger:
        #     min_danger = danger
        #     min_danger_idx = i + 1
        #     # print("-" * xmax)
        #     # show(robots, xmax, ymax)

    return part_one, min_danger_idx


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    if input_file == "./test.txt":
        xmax, ymax = 11, 7
    else:
        xmax, ymax = 101, 103
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.readlines()

    part_one, part_two = solve(lines, xmax, ymax)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
