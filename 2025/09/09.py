import sys
from collections import deque
from time import perf_counter


def get_areas(points: list[tuple[int, int]]) -> dict[tuple[int, int], int]:
    result = {}
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            x1, y1 = points[i]
            x2, y2 = points[j]
            d1 = abs(x2 - x1) + 1
            d2 = abs(y2 - y1) + 1
            area = d1 * d2
            result[(i, j)] = area
    return result


def solve(lines: list[str], x: int) -> tuple[int, int]:
    red_points = []
    xs = []
    ys = []

    # input parsing
    for line in lines:
        x, y = map(int, line.split(","))
        red_points.append((x, y))
        xs.append(x)
        ys.append(y)

    # map corners to their areas
    areas = get_areas(red_points)

    # coordinate compression
    xs = {x: ix for ix, x in enumerate(sorted(set(xs)), start=1)}
    ys = {y: ix for ix, y in enumerate(sorted(set(ys)), start=1)}
    red_points_mapped = [(xs[x], ys[y]) for (x, y) in red_points]
    green_points_mapped = []
    n_points = len(red_points_mapped)
    for i in range(len(red_points_mapped)):
        x1, y1 = red_points_mapped[i]
        x2, y2 = red_points_mapped[(i + 1) % n_points]
        if x1 == x2:
            for yy in range(min(y1, y2) + 1, max(y1, y2)):
                green_points_mapped.append((x1, yy))
        else:
            for xx in range(min(x1, x2) + 1, max(x1, x2)):
                green_points_mapped.append((xx, y1))
    min_x = 1
    min_y = 1
    max_x = len(xs)
    max_y = len(xs)

    # flood fill
    boundary_mapped = set(red_points_mapped).union(green_points_mapped)
    outside_mapped = set()
    queue = deque()
    queue.append((min_x - 1, min_y - 1))
    explored = {(min_x - 1, min_y - 1)}
    while queue:
        x, y = queue.pop()
        outside_mapped.add((x, y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            xx, yy = x + dx, y + dy

            if (
                (min_x - 1 <= xx <= max_x + 1)
                and (min_y - 1 <= yy <= max_y + 1)
                and ((xx, yy) not in boundary_mapped)
                and ((xx, yy) not in outside_mapped)
                and ((xx, yy) not in explored)
            ):
                queue.append((xx, yy))
            explored.add((xx, yy))

    # solve
    part_two = 0
    for ix, ((i, j), area) in enumerate(
        sorted(areas.items(), reverse=True, key=lambda x: x[1])
    ):
        if ix == 0:
            part_one = area
        x1, y1 = red_points_mapped[i]
        x2, y2 = red_points_mapped[j]
        viable = True
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if (x, y) in outside_mapped:
                    viable = False
                    break
            if not viable:
                break
        if viable:
            part_two = area
            break

    return part_one, part_two


if __name__ == "__main__":
    input_file, x = (sys.argv[1], 1000) if len(sys.argv) > 1 else ("./test.txt", 10)
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines, x)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
