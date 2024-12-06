import sys
from time import perf_counter

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def solve(lines: list[str]) -> tuple[int, int]:
    xmax = len(lines[0])
    ymax = len(lines)
    for y, line in enumerate(lines):
        try:
            # guard starts facing up in both test and real input
            x = line.index("^")
            break
        except ValueError:
            pass

    def get_journey_length(
        x: int,
        y: int,
        dir_index: int,
        obs_x: int | None = None,
        obs_y: int | None = None,
    ) -> dict[tuple[int, int, int, int], tuple[int, int]]:
        visited = {}
        dx, dy = DIRS[dir_index]
        while True:
            if (x, y, dx, dy) in visited:
                raise RuntimeError("loop!")
            visited[(x, y, dx, dy)] = (x, y)
            next_x, next_y = x + dx, y + dy
            if not (0 <= next_x < xmax and 0 <= next_y < ymax):
                break
            elif (lines[next_y][next_x] == "#") or (next_x, next_y) == (obs_x, obs_y):
                dir_index = (dir_index + 1) % 4
                dx, dy = DIRS[dir_index]
            else:
                x, y = next_x, next_y
        return visited

    # dir_index is 0 because we're facing up
    part_one_dict = get_journey_length(x, y, 0)
    part_one = len(set(part_one_dict.values()))
    del part_one_dict[(x, y, 0, -1)]  # don't put obstacle at starting position
    solutions = set()
    checked = set()
    last_dir = (0, -1)
    last_x, last_y = (x, y)
    for obs_x, obs_y, dx, dy in part_one_dict:
        if ((obs_x, obs_y) not in checked) and ((obs_x, obs_y) != (last_x, last_y)):
            try:
                get_journey_length(
                    x=last_x,
                    y=last_y,
                    dir_index=DIRS.index(last_dir),
                    obs_x=obs_x,
                    obs_y=obs_y,
                )
            except RuntimeError:
                solutions.add((obs_x, obs_y))
        checked.add((obs_x, obs_y))
        last_dir = (dx, dy)
        last_x, last_y = obs_x, obs_y

    return part_one, len(solutions)


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
