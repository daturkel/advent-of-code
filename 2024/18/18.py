from __future__ import annotations

import heapq
import sys
from collections import defaultdict
from time import perf_counter


class Node:
    def __init__(self, x: int, y: int, score: int, parent: Node | None):
        self.coords = (x, y)
        self.score = score
        self.parent = parent

    def __lt__(self, other: Node):
        return (self.score, *self.coords) < (other.score, *other.coords)


def djikstra(grid: list[list[str]]) -> tuple[float, set[tuple[int, int]]]:
    distances: defaultdict[tuple[int, int], float] = defaultdict(lambda: float("inf"))
    origin = Node(0, 0, 0, None)
    distances[origin.coords] = 0
    queue = [origin]
    min_dist = float("inf")
    while queue:
        node = heapq.heappop(queue)
        x, y = node.coords
        score = node.score
        for nx, ny in [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]:
            if not ((0 <= nx < dim) and (0 <= ny < dim)):
                continue
            if grid[ny][nx] != "#":
                neighbor = Node(nx, ny, score + 1, node)
                if nx == ny == dim - 1:
                    min_dist = score + 1
                    break
                elif score + 1 < distances[neighbor.coords]:
                    heapq.heappush(queue, neighbor)
                    distances[neighbor.coords] = score + 1

    point_set = set([neighbor.coords])
    while neighbor.parent is not None:
        neighbor = neighbor.parent
        point_set.add(neighbor.coords)

    return min_dist, point_set


def solve(lines: list[str], dim: int, n_bytes: int) -> tuple[int, str]:
    grid = [["."] * dim for _ in range(dim)]
    for i, line in enumerate(lines):
        if i >= n_bytes:
            break
        x, y = line.split(",", 1)
        x = int(x)
        y = int(y)
        grid[y][x] = "#"

    part_one, point_set = djikstra(grid)
    part_one = int(part_one)

    for i, line in enumerate(lines[n_bytes:]):
        x, y = line.split(",", 1)
        x = int(x)
        y = int(y)
        grid[y][x] = "#"
        if (x, y) in point_set:
            min_dist, point_set = djikstra(grid)
            if min_dist == float("inf"):
                break

    return part_one, f"{x},{y}"


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    if input_file == "./test.txt":
        dim = 7
        n_bytes = 12
    else:
        dim = 71
        n_bytes = 1024

    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines, dim, n_bytes)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
