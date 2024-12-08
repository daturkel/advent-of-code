import sys
from collections import defaultdict
from itertools import combinations
from time import perf_counter


def solve(lines: list[str]) -> tuple[int, int]:
    nodes = defaultdict(set)
    xmax = len(lines[0])
    ymax = len(lines)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ".":
                nodes[char].add((x, y))
    antinodes_a = set()
    antinodes_b = set()
    for node_set in nodes.values():
        for (ax, ay), (bx, by) in combinations(node_set, 2):
            dx = bx - ax
            dy = by - ay
            antinodes_b.add((ax, ay))
            antinodes_b.add((bx, by))
            xx = ax - dx
            yy = ay - dy
            first = True
            while 0 <= xx < xmax and 0 <= yy < ymax:
                if first:
                    antinodes_a.add((xx, yy))
                else:
                    antinodes_b.add((xx, yy))
                xx -= dx
                yy -= dy
            xx = bx + dx
            yy = by + dy
            while 0 <= xx < xmax and 0 <= yy < ymax:
                if first:
                    antinodes_a.add((xx, yy))
                else:
                    antinodes_b.add((xx, yy))
                xx += dx
                yy += dy
        antinodes_b = antinodes_b.union(antinodes_a)
    return len(antinodes_a), len(antinodes_b)


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
