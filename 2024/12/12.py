import sys
from time import perf_counter


def solve(lines: list[str]) -> tuple[int, int]:
    xmax = len(lines[0])
    ymax = len(lines)
    visited: set[tuple[int, int]] = set()

    def get_area_and_perimiter(
        x0: int, y0: int, visited: set[tuple[int, int]], lines: list[str]
    ) -> tuple[int, int, set[tuple[int, int]]]:
        char = lines[y0][x0]
        to_visit = [(x0, y0)]
        region = set([(x0, y0)])
        perimeter = 0
        while to_visit:
            x, y = to_visit.pop()
            visited.add((x, y))
            for xx, yy in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                if 0 <= xx < xmax and 0 <= yy < ymax:
                    if (xx, yy) in region:
                        pass
                    elif (xx, yy) in visited:
                        perimeter += 1
                    elif lines[yy][xx] == char:
                        to_visit.append((xx, yy))
                        region.add((xx, yy))
                    else:
                        perimeter += 1
                else:
                    perimeter += 1
        return len(region), perimeter, visited

    cost = 0

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if (x, y) not in visited:
                area, perimeter, visited = get_area_and_perimiter(x, y, visited, lines)
                cost += area * perimeter

    return cost, 0


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
