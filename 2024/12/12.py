import sys
from dataclasses import dataclass
from time import perf_counter
from typing import Literal


# we only mutate during post_init so unsafe_hash is ok
@dataclass(frozen=True)
class Edge:
    x: int
    y: int
    dir: Literal["N", "S", "E", "W"]


def solve(lines: list[str]) -> tuple[int, int]:
    xmax = len(lines[0])
    ymax = len(lines)
    visited: set[tuple[int, int]] = set()

    def get_area_and_perimiter(
        x0: int, y0: int, visited: set[tuple[int, int]], lines: list[str]
    ) -> tuple[int, int, int, set[tuple[int, int]]]:
        char = lines[y0][x0]
        to_visit = [(x0, y0)]
        region = set([(x0, y0)])
        perimeter: set[Edge] = set()
        # perimeter = 0
        while to_visit:
            x, y = to_visit.pop()
            visited.add((x, y))
            for xx, yy, dir_ in [
                (x - 1, y, "W"),
                (x + 1, y, "E"),
                (x, y - 1, "N"),
                (x, y + 1, "S"),
            ]:
                if 0 <= xx < xmax and 0 <= yy < ymax:
                    if (xx, yy) in region:
                        pass
                    elif (xx, yy) in visited:
                        perimeter.add(Edge(x, y, dir_))  # type: ignore
                    elif lines[yy][xx] == char:
                        to_visit.append((xx, yy))
                        region.add((xx, yy))
                    else:
                        perimeter.add(Edge(x, y, dir_))  # type: ignore
                else:
                    perimeter.add(Edge(x, y, dir_))  # type: ignore

        len_perimeter = len(perimeter)

        num_sides = 0
        while perimeter:
            edge = perimeter.pop()
            num_sides += 1
            if edge.dir in ("N", "S"):
                dx, dy = 1, 0
            else:
                dx, dy = 0, 1

            xx = edge.x - dx
            yy = edge.y - dy
            while xx >= 0 and yy >= 0:
                next_edge = Edge(xx, yy, edge.dir)
                if next_edge in perimeter:
                    perimeter.remove(next_edge)
                    xx -= dx
                    yy -= dy
                else:
                    break
            xx = edge.x + dx
            yy = edge.y + dy
            while xx < xmax and yy < ymax:
                next_edge = Edge(xx, yy, edge.dir)
                if next_edge in perimeter:
                    perimeter.remove(next_edge)
                    xx += dx
                    yy += dy
                else:
                    break

        return len(region), len_perimeter, num_sides, visited

    cost_one = 0
    cost_two = 0

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if (x, y) not in visited:
                area, perimeter, num_sides, visited = get_area_and_perimiter(
                    x, y, visited, lines
                )
                cost_one += area * perimeter
                cost_two += area * num_sides

    return cost_one, cost_two


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
