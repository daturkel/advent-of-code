from __future__ import annotations

import sys
from collections import deque
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


def solve(lines: list[str]) -> tuple[int, int]:
    xmax = len(lines[0]) - 1
    ymax = len(lines) - 1
    x0 = 1
    y0 = len(lines) - 2

    end = (xmax - 1, 1)

    queue: deque[Node] = deque()
    root = Node(x0, y0, 1, 0, xmax, ymax)
    queue.append(root)
    ends = []
    score = float("inf")
    while queue:
        print(score)
        node = queue.popleft()
        if (node.x, node.y) == end:
            ends.append(node)
            score = node.score
        for neighbor in node.neighbors():
            if neighbor.score > score:
                continue
            if lines[neighbor.y][neighbor.x] != "#":
                queue.append(neighbor)

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
