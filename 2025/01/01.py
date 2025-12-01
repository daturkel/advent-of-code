import sys
from time import perf_counter


def solve(lines: list[str]) -> tuple[int, int]:
    position = 50
    exact_zeros = 0
    passing_zeros = 0
    for line in lines:
        sign = -1 if line[0] == "L" else 1
        turn = int(line[1:])
        abs_turn = abs(turn)
        # guaranteed zero passes
        passes = abs_turn // 100
        remaining_turn = abs_turn % 100
        # potential extra zero passes due to starting offset
        if sign == -1 and remaining_turn >= position and position != 0:
            passes += 1
        elif sign == 1 and remaining_turn >= (100 - position):
            passes += 1
        position = (position + sign * turn) % 100
        if position == 0:
            exact_zeros += 1
        passing_zeros += passes
    return exact_zeros, passing_zeros


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{part_one=}, {part_two=} ({time_us}µs)")
