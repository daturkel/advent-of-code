import sys
from math import prod
from time import perf_counter


def solve(lines: list) -> tuple[int, int]:
    part_one = 0
    part_two = 0
    lines[:-1] = [map(int, line.split()) for line in lines[:-1]]
    operand_list = zip(*lines[:-1])
    for operator, operands in zip(lines[-1].split(), operand_list):
        if operator == "+":
            part_one += sum(operands)
        else:
            part_one += prod(operands)

    return part_one, part_two


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
