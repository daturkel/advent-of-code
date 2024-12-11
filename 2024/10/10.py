import sys
from time import perf_counter

Point = tuple[int, int]


def solve(lines: list[str]) -> Point:
    zeros = set()
    xmax = len(lines[0])
    ymax = len(lines)
    grid: list[list[int]] = [[int(n) for n in line] for line in lines]
    # find the zeros
    for y, line in enumerate(grid):
        for x, num in enumerate(line):
            if num == 0:
                zeros.add((x, y))

    # DFS with cache
    def paths_to_end(
        x: int, y: int, cache: dict[Point, tuple[set[Point], int]] = {}
    ) -> tuple[set[Point], int]:
        if (x, y) in cache:
            return cache[(x, y)]
        rating = 0  # ways to reach any 9
        ends = set()  # unique 9s visited
        value = grid[y][x]
        for xx, yy in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if 0 <= xx < xmax and 0 <= yy < ymax:
                if grid[yy][xx] == 9 == value + 1:
                    rating += 1
                    ends.add((xx, yy))
                elif grid[yy][xx] == value + 1:
                    new_ends, new_rating = paths_to_end(xx, yy)
                    rating += new_rating
                    ends = ends.union(new_ends)
        cache[(x, y)] = ends, rating
        return ends, rating

    part_one = 0
    part_two = 0

    for x0, y0 in zeros:
        ends, rating = paths_to_end(x0, y0)
        part_one += len(ends)
        part_two += rating

    return part_one, part_two


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
