from __future__ import annotations

import sys
from collections import defaultdict
from heapq import heappop, heappush
from time import perf_counter
from typing import NamedTuple

Point = tuple[int, int]


class PriorityQueue:
    def __init__(self):
        self._pq = []
        self.lookup = {}

    def add_update(self, node, priority):
        if node in self.lookup:
            self.remove(node)
        entry = [priority, node]
        self.lookup[node] = entry
        heappush(self._pq, entry)

    def remove(self, node):
        entry = self.lookup.pop(node)
        entry[0] = None

    def pop(self):
        while self._pq:
            priority, node = heappop(self._pq)
            if node is not None:
                del self.lookup[node]
                return node
        raise KeyError("pop from empty pq")


# point, direction we're moving, and steps from that direction
class Node(NamedTuple):
    point: Point
    direction: str
    steps: int


DIRECTIONS = {"E": (1, 0), "W": (-1, 0), "N": (0, -1), "S": (0, 1)}
OPPOSITES = {"E": "W", "W": "E", "N": "S", "S": "N", "": ""}


def get_neighbors(node: Node, width: int, height: int) -> list[Node]:
    x, y = node.point
    neighbors = []

    for direction, (dx, dy) in DIRECTIONS.items():
        if direction == OPPOSITES[node.direction]:
            continue
        if not (0 <= x + dx < width) or not (0 <= y + dy < height):
            continue
        if (direction == node.direction) and (node.steps < 3):
            neighbors.append(Node((x + dx, y + dy), direction, node.steps + 1))
        elif direction != node.direction:
            neighbors.append(Node((x + dx, y + dy), direction, 1))

    return neighbors


def dijkstra(start: Point, end: Point, grid: list[list[int]]) -> tuple[int, dict, Node]:
    distances = defaultdict(lambda: float("inf"))
    current_node = Node(start, "", 0)
    width = len(grid[0])
    height = len(grid)
    # for direction in ["E", "W", "N", "S"]:
    #     for steps in [1, 2, 3]:
    #         for x in range(width):
    #             for y in range(height):
    #                 distances[Node((x, y), direction, steps)] = float("inf")
    visited = set()

    distances[current_node] = 0
    prev = {}

    while True:
        visited.add(current_node)
        current_distance = distances[current_node]
        for neighbor_node in get_neighbors(current_node, width, height):
            nx, ny = neighbor_node.point
            possible_distance = current_distance + grid[ny][nx]
            if possible_distance < distances[neighbor_node]:
                distances[neighbor_node] = possible_distance
                prev[neighbor_node] = current_node
                if (nx, ny) == end:
                    return int(possible_distance), prev, neighbor_node
        current_node = min(
            [node for node in distances if node not in visited],
            key=lambda k: distances[k],
        )


def solve(lines: list[str]) -> tuple[int, int]:
    grid = [[int(char) for char in row] for row in lines]
    start = (0, 0)
    end = (len(grid[0]) - 1, len(grid) - 1)
    min_heat_loss, prev, end_node = dijkstra(start, end, grid)
    current = end_node
    print("solved")
    while current.point != start:
        x, y = current.point
        grid[y][x] = "*"  # type: ignore
        current = prev[current]

    for row in grid:
        print("".join([str(num) for num in row]))

    return min_heat_loss, 0


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    min_heat_loss, new_ways_to_win = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{min_heat_loss=}, {new_ways_to_win=} ({time_us}ms)")
