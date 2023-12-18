from __future__ import annotations

import sys
from collections import defaultdict
from heapq import heappop, heappush
from itertools import count
from time import perf_counter
from typing import Callable, NamedTuple

Point = tuple[int, int]


class PriorityQueue:
    def __init__(self):
        self._pq = []
        self.lookup = {}
        self._counter = count()

    def add_update(self, node, priority):
        if node in self.lookup:
            self.remove(node)
        entry = [priority, next(self._counter), node]
        self.lookup[node] = entry
        heappush(self._pq, entry)

    def remove(self, node):
        entry = self.lookup.pop(node)
        entry[2] = None

    def pop(self):
        while self._pq:
            priority, _, node = heappop(self._pq)
            if node is not None:
                del self.lookup[node]
                return node
        raise KeyError("pop from empty pq")

    def get(self, node):
        return self.lookup[node][0]


# point, direction we're moving, and steps from that direction
class Node(NamedTuple):
    point: Point
    direction: str
    steps: int


DIRECTIONS = {"E": (1, 0), "W": (-1, 0), "N": (0, -1), "S": (0, 1)}
OPPOSITES = {"E": "W", "W": "E", "N": "S", "S": "N", "": ""}


def get_neighbors_a(node: Node, width: int, height: int) -> list[Node]:
    x, y = node.point
    neighbors = []

    for direction, (dx, dy) in DIRECTIONS.items():
        if direction == OPPOSITES[node.direction]:
            continue
        if not (0 <= x + dx < width) or not (0 <= y + dy < height):
            continue
        if (direction == node.direction) and (node.steps < 3):
            neighbors.append(Node((x + dx, y + dy), direction, node.steps + 1))
        if direction != node.direction:
            neighbors.append(Node((x + dx, y + dy), direction, 1))

    return neighbors


def get_neighbors_b(node: Node, width: int, height: int) -> list[Node]:
    x, y = node.point
    neighbors = []

    for direction, (dx, dy) in DIRECTIONS.items():
        if direction == OPPOSITES[node.direction]:
            continue
        if not (0 <= x + dx < width) or not (0 <= y + dy < height):
            continue
        if (direction == node.direction) and (node.steps < 10):
            neighbors.append(Node((x + dx, y + dy), direction, node.steps + 1))
        elif (direction != node.direction) and (node.steps >= 4):
            neighbors.append(Node((x + dx, y + dy), direction, 1))
        elif node.direction == "":
            neighbors.append(Node((x + dx, y + dy), direction, 1))

    return neighbors


def dijkstra(
    start: Point,
    end: Point,
    grid: list[list[int]],
    neighbor_fn: Callable[[Node, int, int], list[Node]],
    min_stop: int = 0,
) -> int:
    distances = defaultdict(lambda: float("inf"))
    pq = PriorityQueue()
    width = len(grid[0])
    height = len(grid)
    current_node = Node(start, "", 0)
    pq.add_update(current_node, float("inf"))
    distances[current_node] = 0

    while True:
        current_distance = distances[current_node]
        for neighbor_node in neighbor_fn(current_node, width, height):
            nx, ny = neighbor_node.point
            possible_distance = current_distance + grid[ny][nx]
            if possible_distance < distances[neighbor_node]:
                distances[neighbor_node] = possible_distance
                pq.add_update(neighbor_node, possible_distance)
                if ((nx, ny) == end) and (neighbor_node.steps > min_stop):
                    return int(possible_distance)
        current_node = pq.pop()


def solve(lines: list[str]) -> tuple[int, int]:
    grid = [[int(char) for char in row] for row in lines]
    start = (0, 0)
    end = (len(grid[0]) - 1, len(grid) - 1)
    min_heat_loss = dijkstra(start, end, grid, get_neighbors_a)
    min_heat_loss_ultra = dijkstra(start, end, grid, get_neighbors_b, 4)

    return min_heat_loss, min_heat_loss_ultra


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    min_heat_loss, new_ways_to_win = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic), 1)

    print(f"{min_heat_loss=}, {new_ways_to_win=} ({time_us}s)")
