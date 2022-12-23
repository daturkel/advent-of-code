#!/usr/bin/env python3

from collections import defaultdict
import sys
from time import perf_counter

Point = tuple[int, int]

DIRS = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
DIR_TO_INDEX = {"N": (0, 3), "E": (2, 5), "S": (4, 7), "W": (6, 9)}


class Grid:
    def __init__(self, lines: list[str]):
        self.rules = ["N", "S", "W", "E"]
        self.elves: dict[int, Point] = {}
        self.grid = {}
        i = 0
        for y in range(len(lines)):
            for x in range(len(lines[0])):
                if lines[y][x] == "#":
                    self.elves[i] = (x, y)
                    i += 1
                    self.grid[(x, y)] = True

    def neighbors(self, elf: Point, cache: dict = {}) -> list[Point]:
        try:
            return cache[elf]
        except KeyError:
            pass

        x, y = elf

        result = [
            (x - 1, y - 1),  # N, W
            (x, y - 1),  # N
            (x + 1, y - 1),  # N, E
            (x + 1, y),  # E
            (x + 1, y + 1),  # E, S
            (x, y + 1),  # S
            (x - 1, y + 1),  # S, W
            (x - 1, y),  # W
            (x - 1, y - 1),  # W, N (repeat this for easier slicing)
        ]

        cache[elf] = result

        return result

    def can_move(self, elf: Point) -> list[Point] | None:
        can_move = False
        neighbors = self.neighbors(elf)
        for neighbor in neighbors:
            if self.grid.get(neighbor, False):
                return neighbors

        return None

    def propose(self, elf: Point, neighbors: list[Point]) -> Point:
        proposal = elf
        # turn neighbor coordinates into a False if there's an elf there and a True if not
        neighbor_bools = [not self.grid.get(neighbor, False) for neighbor in neighbors]
        for rule in self.rules:
            index = DIR_TO_INDEX[rule]
            these_neighbors = neighbor_bools[index[0] : index[1]]
            # if all neighboring spots are not elves
            if all(neighbor_bool for neighbor_bool in these_neighbors):
                dx, dy = DIRS[rule]
                proposal = (elf[0] + dx, elf[1] + dy)
                break

        return proposal

    def proposals(self) -> defaultdict[Point, list[int]]:
        proposals = defaultdict(list)
        for idx, elf in self.elves.items():
            can_move = self.can_move(elf)
            if can_move:
                proposal = self.propose(elf, can_move)
                proposals[proposal].append(idx)

        return proposals

    def round(self) -> bool:
        changed = False
        proposals = self.proposals()
        for new_point, old_points in proposals.items():
            if len(old_points) > 1:
                continue
            changed = True
            idx = old_points[0]
            old_point = self.elves[idx]
            self.elves[idx] = new_point
            del self.grid[old_point]
            self.grid[new_point] = True
        self.rules = self.rules[1:] + [self.rules[0]]

        return changed

    def count_tiles(self) -> int:
        current_elves = self.elves.values()
        min_x = min(elf[0] for elf in current_elves)
        min_y = min(elf[1] for elf in current_elves)
        max_x = max(elf[0] for elf in current_elves)
        max_y = max(elf[1] for elf in current_elves)
        return (max_y - min_y + 1) * (max_x - min_x + 1) - len(self.elves)


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
