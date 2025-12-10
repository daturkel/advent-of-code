import sys
from time import perf_counter


def get_max_area(points: list[tuple[int, int]]) -> int:
    result = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            x1, y1 = points[i]
            x2, y2 = points[j]
            d1 = abs(x2 - x1) + 1
            d2 = abs(y2 - y1) + 1
            area = d1 * d2
            if area >= result:
                result = area
    return result


def solve(lines: list[str], x: int) -> tuple[int, int]:
    part_one = 0
    part_two = 0
    red_points = []
    green_points = set()
    min_x = 10000000000
    max_x = 0
    min_y = 10000000000
    max_y = 0
    for line in lines:
        x, y = map(int, line.split(","))
        min_x = min(x, min_x)
        max_x = max(x, max_x)
        min_y = min(y, min_y)
        max_y = max(y, max_y)
        red_points.append((x, y))
        if len(red_points) > 1:
            old_x, old_y = red_points[-2]
            if old_x == x:
                for yy in range(min(old_y, y) + 1, max(old_y, y)):
                    green_points.add((x, yy))
            else:
                for xx in range(min(old_x, x) + 1, max(old_x, x)):
                    green_points.add((xx, y))
    boundary_points = set(red_points).union(green_points)
    for y in range(min_y, max_y + 1):
        inside = False
        for x in range(min_x, max_x + 1):
            if inside and (x, y) not in boundary_points:
                inside = False

    inside = set()

    part_one = get_max_area(red_points)
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
