import re
import sys
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

    def get_quadrant(self, xmax: int, ymax: int) -> int | None:
        if self.x < xmax // 2:
            if self.y < ymax // 2:
                return 0
            elif self.y > ymax // 2:
                return 1
        elif self.x > xmax // 2:
            if self.y < ymax // 2:
                return 2
            elif self.y > ymax // 2:
                return 3


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

    quadrants = [0, 0, 0, 0]
    for robot in robots:
        robot.move(100, xmax, ymax)
        quadrant = robot.get_quadrant(xmax, ymax)
        if quadrant is not None:
            quadrants[quadrant] += 1

    part_one = 1
    for quadrant in quadrants:
        part_one *= quadrant
    print("-" * xmax)

    return part_one, 0


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
