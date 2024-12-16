from __future__ import annotations

import heapq
import sys
from collections import defaultdict
from dataclasses import dataclass
from time import perf_counter


@dataclass
class Node:
    x: int
    y: int
    dx: int
    dy: int
    xmax: int
    ymax: int
    score: int = 0

    def neighbors(self) -> list[Node]:
        neighbors = []
        for dx, dy in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]:
            if (dx, dy) == (-1 * self.dx, -1 * self.dy):
                continue
            x = self.x + dx
            y = self.y + dy
            if 0 < x < self.xmax and 0 < y < self.ymax:
                score_delta = 1
                if (dx, dy) != (self.dx, self.dy):
                    score_delta += 1000
                neighbors.append(
                    Node(
                        x=x,
                        y=y,
                        dx=dx,
                        dy=dy,
                        xmax=self.xmax,
                        ymax=self.ymax,
                        score=self.score + score_delta,
                    )
                )

        return neighbors

    # this class needs to be comparable in order to break ties in the queue
    def __lt__(self, other):
        return self.score < other.score


def show(lines, x, y, score, visited):
    print(score)
    for yy, line in enumerate(lines):
        row = []
        for xx, char in enumerate(line):
            if (xx, yy) == (x, y):
                row.append("X")
            elif (xx, yy) in visited:
                row.append("O")
            else:
                row.append(char)
        print("".join(row))


def solve(lines: list[str]) -> tuple[int, int]:
    xmax = len(lines[0]) - 1
    ymax = len(lines) - 1
    x0 = 1
    y0 = len(lines) - 2
    end = (xmax - 1, 1)

    distances = defaultdict(lambda: float("inf"))
    distances[(x0, y0)] = 0

    queue = [Node(x0, y0, 1, 0, xmax, ymax)]
    ends = []
    visited = set()
    score = float("inf")
    while queue:
        node = heapq.heappop(queue)
        visited.add((node.x, node.y))
        show(lines, node.x, node.y, node.score, visited)
        input()
        if (node.x, node.y) == end:
            ends.append(node)
            score = node.score
        for neighbor in node.neighbors():
            if lines[neighbor.y][neighbor.x] != "#":
                if (
                    neighbor.score <= distances[(neighbor.x, neighbor.y)]
                    and neighbor.score < score
                ):
                    heapq.heappush(queue, neighbor)
                    distances[(neighbor.x, neighbor.y)] = neighbor.score

    print(ends)
    for end in ends:
        score = min(score, end.score)

    return int(score), 0


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
