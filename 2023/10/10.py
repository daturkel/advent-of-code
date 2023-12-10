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

Pair = tuple[int, int]
SetOfPairs = set[Pair]

# If the beginning and end of hitting a border are one of these pairs, you've crossed it
VALID_CROSSINGS = {
    frozenset({"|"}),
    frozenset({"-"}),
    frozenset({"J", "F"}),
    frozenset(["L", "7"]),
}


def check_point(
    x: int,
    y: int,
    border: SetOfPairs,
    outside: SetOfPairs,
    inside: SetOfPairs,
    lines: list[str],
    width: int,
    height: int,
) -> tuple[SetOfPairs, SetOfPairs]:
    """Returns inside and outside with (x,y) added to one of them"""
    point = (x, y)
    # ----------------- figure out which direction we should look in ----------------- #
    dw = x
    dn = y
    de = width - x
    ds = height - y
    nearest = min(dw, dn, de, ds)
    if nearest == dw:
        dir_ = "W"
    elif nearest == dn:
        dir_ = "N"
    elif nearest == de:
        dir_ = "E"
    else:
        dir_ = "S"
    dx, dy = DIR_TO_DXDY[dir_]
    # ---------------------------- move in that direction ---------------------------- #
    num_crosses = 0
    in_border = False
    border_start = None
    border_end = None
    while True:
        x, y = x + dx, y + dy
        if (0 <= x < width) and (0 <= y < height):
            neighbor = lines[y][x]
        # if we hit the edge, count the number of times we've crossed to see if we're inside
        else:
            if num_crosses % 2 == 0:
                outside.add(point)
            else:
                inside.add(point)
            break

        # shortcuts to stop early if we hit a known outside or known inside
        if ((x, y) in outside) and (num_crosses % 2 == 0):
            # we've crossed an even amount of times and hit a known outside
            outside.add(point)
            break
        elif ((x, y) in inside) and (num_crosses == 0):
            # we've hit a known inside without any crossings
            inside.add(point)
            break
        elif (x, y) in border:
            if not in_border:
                border_start = neighbor
                in_border = True
            # `dir_ not in PIECES_TO_DIRS[neighbor]` means we're leaving the border because
            # this border piece doesn't go in the direction we're going
            if in_border and dir_ not in PIECE_TO_DIRS[neighbor]:
                border_end = neighbor
                in_border = False
                if frozenset({border_start, border_end}) in VALID_CROSSINGS:
                    num_crosses += 1
    return outside, inside


def solve(raw_lines: str) -> tuple[int, int]:
    # --------------------------- figure out starting point -------------------------- #
    si = raw_lines.index("S")
    sy = raw_lines[:si].count("\n")  # get y coordinate
    width = raw_lines.index("\n")
    sx = (si - sy) % width  # get x coordinate
    lines = raw_lines.split("\n")
    starting_dirs = set([])
    starting_piece = "S"
    for dir_ in "SENW":
        dx, dy = DIR_TO_DXDY[dir_]
        try:
            neighbor = lines[sy + dy][sx + dx]
            if neighbor in DIR_TO_VALID_PIECES[dir_]:
                starting_dirs.add(dir_)
        except IndexError:
            continue
    for piece, dirs in PIECE_TO_DIRS.items():
        if dirs == starting_dirs:
            starting_piece = piece
            break
    lines[sy] = lines[sy].replace("S", starting_piece)
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
    # ------------------------------------ part 2 ------------------------------------ #
    border = set(distances.keys())
    border.add((sx, sy))
    outside = set([])
    inside = set([])
    height = len(lines)

    # it might be more efficient to spiral from the outside inward (to be more likely to
    # stop early for hitting known outside locations), but this is fast enough
    for x in range(width):
        for y in range(height):
            if (x, y) in border:
                continue
            else:
                outside, inside = check_point(
                    x, y, border, outside, inside, lines, width, height
                )

    num_inside = len(inside)

    return max_distance, num_inside


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        raw_lines = file.read()

    max_distance, num_inside = solve(raw_lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{max_distance=}, {num_inside=} ({time_us}ms)")
