import sys
from itertools import product
from time import perf_counter


def parse_obj(lines: list[str]) -> tuple[int, int, int, int, int]:
    nums = [-1, -1, -1, -1, -1]
    for i in range(5):
        for row in lines:
            if row[i] == "#":
                nums[i] += 1
            else:
                break

    return tuple(nums)  # type: ignore


def solve(lines: list[str]) -> tuple[int, int]:
    locks = []
    keys = []
    while lines:
        sample, lines = lines[:7], lines[8:]
        if sample[0] == "#####":
            locks.append(parse_obj(sample))
        else:
            keys.append(parse_obj(sample[::-1]))

    part_one = 0
    for key, lock in product(keys, locks):
        valid = True
        for i in range(5):
            if key[i] + lock[i] >= 6:
                valid = False
                break
        if valid:
            part_one += 1

    return part_one, 0


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
