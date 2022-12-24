#!/usr/bin/env python3

from collections import deque
import sys
from time import perf_counter

Point = tuple[int, int]
Storm = tuple[Point, Point]

DIR_MAP = {"v": (0, 1), "^": (0, -1), "<": (-1, 0), ">": (1, 0)}


class Grid:
    def __init__(self, lines: list[str]):
        lines = lines[1:-1]  # strip off top and bottom rows
        lines = [line[1:-1] for line in lines]  # strip off first and last columns
        self.width = len(lines[0])
        self.height = len(lines)
        self.storms = []
        for y in range(len(lines)):
            for x in range(len(lines[0])):
                char = lines[y][x]
                if char in "v^<>":
                    self.storms.append(((x, y), DIR_MAP[char]))
        self.start = (0, -1)
        self.end = (self.width - 1, self.height)
        self.goals = [self.end, self.start, self.end]

    def storm_points_at_t(self, t: int, cache: dict = {}) -> set[Point]:
        """Return the coordinates of storms at time t."""
        if t in cache:
            return cache[t]

        result = set()
        for storm in self.storms:
            sx, sy = storm[0]
            dx, dy = storm[1]
            nx = (sx + t * dx) % self.width
            ny = (sy + t * dy) % self.height
            result.add((nx, ny))

        cache[t] = result

        return result

    def neighbors(self, point: Point, cache: dict = {}) -> list[Point]:
        if point in cache:
            return cache[point]

        x, y = point
        candidates = [point, (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        result = [
            (x, y)
            for x, y in candidates
            if ((0 <= x < self.width) and (0 <= y < self.height))
            or ((x, y) == self.start)
            or ((x, y) == self.end)
        ]
        cache[point] = result

        return result

    def navigate(self) -> tuple[int, int]:
        explored = set([(self.start, 0)])
        queue: deque[tuple[Point, int]] = deque()
        queue.append((self.start, 0))
        times = []

        goal_idx = 0
        goal = self.goals[goal_idx]

        while queue:
            current, t = queue.popleft()
            # cycle through our three goals
            if current == goal:
                times.append(t)
                goal_idx += 1
                queue = deque()
                explored = set([(current, t)])
                try:
                    goal = self.goals[goal_idx]
                except IndexError:
                    # stop if we hit all three goals
                    break

            storm_pts = self.storm_points_at_t(t + 1)
            neighbors = self.neighbors(current)
            for neighbor in neighbors:
                # NOTE: A potential speedup is to only check the storms that could possible
                # interfere with this particular neighbor.
                if (neighbor not in storm_pts) and ((neighbor, t + 1) not in explored):
                    queue.append((neighbor, t + 1))
                    explored.add((neighbor, t + 1))

        # only care about first and third time
        return times[0], times[2]


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = [line.rstrip() for line in file.readlines()]

    tic = perf_counter()
    grid = Grid(lines)
    part_a, part_b = grid.navigate()

    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_a=}, {part_b=} ({time_us}ms)")
