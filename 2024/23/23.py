import sys
from collections import defaultdict
from itertools import combinations
from time import perf_counter


def is_connected(nodes: list[str], graph: defaultdict[str, set]) -> bool:
    while nodes:
        node = nodes.pop()
        for other in nodes:
            if other not in graph[node]:
                return False
    return True


def solve(lines: list[str]) -> tuple[int, str]:
    graph: defaultdict[str, set] = defaultdict(set)
    for line in lines:
        node_a, node_b = line.split("-")
        graph[node_a].add(node_b)
        graph[node_b].add(node_a)

    parties_of_three = set()
    biggest_party = []
    for node, neighbors in graph.items():
        if not node.startswith("t"):
            continue
        for neighbor_a, neighbor_b in combinations(neighbors, 2):
            if neighbor_b in graph[neighbor_a]:
                parties_of_three.add(tuple(sorted((node, neighbor_a, neighbor_b))))
        for n in range(len(neighbors), 0, -1):
            if n < len(biggest_party):
                continue
            for neighbor_subset in combinations(neighbors, n):
                if is_connected(list(neighbor_subset), graph):
                    biggest_party = [node, *neighbor_subset]

    return len(parties_of_three), ",".join(sorted(biggest_party))


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
