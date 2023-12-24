import sys
from time import perf_counter


def solve(lines: list[str], vmin: int, vmax: int) -> tuple[int, int]:
    eqns = []
    for line in lines:
        point, velocity = line.split(" @ ")
        point = tuple(int(num) for num in point.split(", "))
        velocity = tuple(int(num) for num in velocity.split(", "))
        slope = velocity[1] / velocity[0]
        intercept = -1 * slope * point[0] + point[1]
        eqns.append((slope, intercept, point[0], velocity[0]))

    solutions = []
    for i, (slope_a, intercept_a, x0_a, vx_a) in enumerate(eqns[:-1]):
        for slope_b, intercept_b, x0_b, vx_b in eqns[i + 1 :]:
            # skip parallel paths
            if slope_a - slope_b == 0:
                continue
            x = (intercept_b - intercept_a) / (slope_a - slope_b)
            # skip solutions that happened in the past
            if ((x - x0_a) * vx_a < 0) or ((x - x0_b) * vx_b < 0):
                continue
            y = x * slope_a + intercept_a
            if (vmin <= x <= vmax) and (vmin <= y <= vmax):
                solutions.append((x, y))

    return len(solutions), 0


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    if input_file == "./test.txt":
        vmin = 7
        vmax = 27
    else:
        vmin = 200000000000000
        vmax = 400000000000000
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    number_intersections, initial_position = solve(lines, vmin, vmax)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{number_intersections=}, {initial_position=} ({time_us}ms)")
