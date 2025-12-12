import sys
from time import perf_counter


def solve(lines: list[str]) -> int:
    part_one = 0
    areas = []
    area = 0
    full_area = 0
    for line in lines[:30]:
        if ":" in line:
            continue
        if not line:
            areas.append((area, full_area))
            area = 0
            full_area = 0
        else:
            area += line.count("#")
            full_area += len(line)

    for line in lines[30:]:
        dims, counts = line.split(": ")
        x, y = map(int, dims.split("x"))
        max_area = x * y
        counts = map(int, counts.split(" "))
        this_area_inner = 0
        this_area_outer = 0
        for i, n in enumerate(counts):
            this_area_inner += n * areas[i][0]  # minimum possible area
            this_area_outer += n * areas[i][1]  # maximum possible area
        # if they fit without any packing, we're good
        if this_area_outer <= max_area:
            part_one += 1
        # if they couldn't fit even with perfect packing, no use trying
        elif this_area_inner > max_area:
            continue
        # if we have to figure out optimal packing...
        else:
            raise NotImplementedError

    return part_one


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{part_one=} ({time_us}µs)")
