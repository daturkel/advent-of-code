import heapq
import sys
from collections import defaultdict
from time import perf_counter


def djikstra(grid: list[list[str]]) -> float:
    distances: defaultdict[tuple[int, int], float] = defaultdict(lambda: float("inf"))
    distances[(0, 0)] = 0
    queue = [(0, 0, 0)]
    min_dist = float("inf")
    while queue:
        score, x, y = heapq.heappop(queue)
        for nx, ny in [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]:
            if not ((0 <= nx < dim) and (0 <= ny < dim)):
                continue
            if grid[ny][nx] != "#":
                if nx == ny == dim - 1:
                    min_dist = score + 1
                    break
                elif score + 1 < distances[(nx, ny)]:
                    heapq.heappush(queue, (score + 1, nx, ny))
                    distances[(nx, ny)] = score + 1
    return min_dist


def solve(lines: list[str], dim: int, n_bytes: int) -> tuple[int, str]:
    grid = [["."] * dim for _ in range(dim)]
    for i, line in enumerate(lines):
        if i >= n_bytes:
            break
        x, y = line.split(",", 1)
        x = int(x)
        y = int(y)
        grid[y][x] = "#"

    part_one = int(djikstra(grid))

    for i, line in enumerate(lines[n_bytes:]):
        x, y = line.split(",", 1)
        x = int(x)
        y = int(y)
        grid[y][x] = "#"
        min_dist = djikstra(grid)
        if min_dist == float("inf"):
            print(i)
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
