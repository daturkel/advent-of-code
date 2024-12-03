import re
import sys
from time import perf_counter


def solve(lines: list[str]) -> tuple[int, int]:
    # four capture groups
    # mul(2,4) -> ["2", "4", "", ""]
    # do() -> ["", "", "do()", ""]
    # don't() -> ["", "", "", "don't()"]
    pattern = re.compile(r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))")
    total = 0
    total_alt = 0
    do_active = True
    for line in lines:
        matches = pattern.findall(line)
        for left, right, do, dont in matches:
            if left != "":
                left = int(left)
                right = int(right)
                product = left * right
                total += product
                if do_active:
                    total_alt += product
            elif do != "":
                do_active = True
            else:
                do_active = False

    return total, total_alt


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.readlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
