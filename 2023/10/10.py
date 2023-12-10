import sys
from collections import defaultdict
from time import perf_counter

PIECE_TO_DIRS = {
    "|": {"N", "S"},
    "-": {"E", "W"},
    "L": {"N", "E"},
    "J": {"N", "W"},
    "7": {"S", "W"},
    "F": {"S", "E"},
}

DIR_TO_OPPOSITE = {"N": "S", "S": "N", "E": "W", "W": "E"}

DIR_TO_VALID_PIECES = defaultdict(set)
for piece, dirs in PIECE_TO_DIRS.items():
    for dir_ in dirs:
        opposite_dir = DIR_TO_OPPOSITE[dir_]
        DIR_TO_VALID_PIECES[opposite_dir].add(piece)

DIR_TO_DXDY = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}


def solve(raw_lines: str) -> tuple[int, int]:
    # --------------------------- figure out starting point -------------------------- #
    si = raw_lines.index("S")
    sy = raw_lines[:si].count("\n")  # get y coordinate
    width = raw_lines.index("\n")
    sx = (si - sy) % width  # get x coordinate
    lines = raw_lines.split("\n")
    starting_dirs = set([])
    for dir_ in "SENW":
        dx, dy = DIR_TO_DXDY[dir_]
        try:
            neighbor = lines[sy + dy][sx + dx]
            if neighbor in DIR_TO_VALID_PIECES[dir_]:
                starting_dirs.add(dir_)
        except IndexError:
            continue
    # --------------------------------- navigate maze -------------------------------- #
    x, y = sx, sy
    dir_ = list(starting_dirs)[0]  # pick arbitrary starting direction
    distance = 0
    distances = {}
    while True:
        distance += 1
        dx, dy = DIR_TO_DXDY[dir_]
        x, y = x + dx, y + dy
        if (x, y) == (sx, sy):
            break
        piece = lines[y][x]
        dir_ = list(PIECE_TO_DIRS[piece].difference(DIR_TO_OPPOSITE[dir_]))[0]
        distances[(x, y)] = distance

    max_distance = int((max(distances.values()) + 1) / 2)
    return max_distance, 0


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        raw_lines = file.read()

    max_distance, backward = solve(raw_lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{max_distance=}, {backward=} ({time_us}ms)")
