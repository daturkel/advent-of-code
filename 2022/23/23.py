#!/usr/bin/env python3

from collections import defaultdict
import sys
from time import perf_counter

Point = list[int]

DIRS = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}


class Grid:
    def __init__(self, lines: list[str]):
        self.width = len(lines[0])
        self.height = len(lines)
        self.grid = [list(line) for line in lines]
        self.elves: dict[int, Point] = {}
        i = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == "#":
                    self.elves[i] = [x, y]
                    i += 1
        self.rules = ["N", "S", "W", "E"]

    def grow(self):
        self.width += 2
        self.height += 2
        self.grid = [["."] + line + ["."] for line in self.grid]
        self.grid = [["."] * self.width] + self.grid + [["."] * self.width]
        for elf in self.elves.values():
            elf[0] += 1
            elf[1] += 1

    def shrink(self):
        min_x = min(elf[0] for elf in self.elves.values())
        max_x = max(elf[0] for elf in self.elves.values())
        min_y = min(elf[1] for elf in self.elves.values())
        max_y = max(elf[1] for elf in self.elves.values())
        self.width = max_x - min_x + 1
        self.height = max_y - min_y + 1

        self.grid = [["."] * self.width for i in range(self.height)]
        for elf in self.elves.values():
            elf[0] -= min_x
            elf[1] -= min_y
            self.grid[elf[1]][elf[0]] = "#"

    def show(self):
        for line in self.grid:
            print("".join(line))

    def neighbors(
        self, elf: Point, which: str | None = None, cache: dict = {}
    ) -> list[Point]:
        x, y = elf
        if (x, y, which) in cache:
            return cache[x, y, which]

        if which is None:
            result = [
                [x - 1, y + 1],
                [x - 1, y],
                [x - 1, y - 1],
                [x, y + 1],
                [x, y - 1],
                [x + 1, y + 1],
                [x + 1, y],
                [x + 1, y - 1],
            ]

        elif which == "N":
            result = [[x - 1, y - 1], [x, y - 1], [x + 1, y - 1]]
        elif which == "E":
            result = [[x + 1, y + 1], [x + 1, y], [x + 1, y - 1]]
        elif which == "W":
            result = [[x - 1, y + 1], [x - 1, y], [x - 1, y - 1]]
        else:
            result = [[x - 1, y + 1], [x, y + 1], [x + 1, y + 1]]

        # result = set(
        #     [
        #         [x, y]
        #         for x, y in result
        #         if (0 < x < self.width) and (0 < y < self.height)
        #     ]
        # )
        cache[(x, y, which)] = result

        return result

    def can_move(self, elf: Point) -> bool:
        can_move = False
        for nx, ny in self.neighbors(elf):
            if self.grid[ny][nx] == "#":
                can_move = True
                break

        return can_move

    def propose(self, elf: Point) -> Point:
        proposal = elf
        for rule in self.rules:
            neighbors = self.neighbors(elf, rule)
            if all(self.grid[ny][nx] == "." for nx, ny in neighbors):
                dx, dy = DIRS[rule]
                proposal = [elf[0] + dx, elf[1] + dy]
                break

        return proposal

    def proposals(self) -> defaultdict[tuple[int, ...], list[int]]:
        proposals = defaultdict(list)
        for idx, elf in self.elves.items():
            if self.can_move(elf):
                proposal = self.propose(elf)
                proposals[tuple(proposal)].append(idx)

        return proposals

    def round(self) -> bool:
        self.grow()
        changed = False
        proposals = self.proposals()
        for new_point, old_points in proposals.items():
            if len(old_points) > 1:
                continue
            changed = True
            nx, ny = new_point
            idx = old_points[0]
            self.elves[idx] = [nx, ny]
        self.shrink()
        self.rules = self.rules[1:] + [self.rules[0]]

        return changed

    def count_tiles(self) -> int:
        return self.width * self.height - len(self.elves)


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = [line.rstrip() for line in file.readlines()]

    tic = perf_counter()
    grid = Grid(lines)
    for _ in range(10):
        grid.round()

    tiles = grid.count_tiles()

    rounds = 10
    changed = True
    while changed:
        rounds += 1
        changed = grid.round()

    toc = perf_counter()
    time_us = round((toc - tic))

    print(f"{tiles=}, {rounds=} ({time_us}s)")
