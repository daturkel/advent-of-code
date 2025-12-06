import re
import sys
from math import prod
from time import perf_counter

OP_MAP = {"*": prod, "+": sum}


def solve_alt(lines: list[str]) -> tuple[int, int]:
    # alternative solution, part 1 only
    part_one = 0
    processed_lines = [map(int, line.split()) for line in lines[:-1]]
    operand_list = zip(*processed_lines)
    for operator, operands in zip(lines[-1].split(), operand_list):
        part_one += OP_MAP[operator](operands)
    return part_one, 0


def solve(lines: list[str]) -> tuple[int, int]:
    part_one = 0
    part_two = 0

    num_operands = len(lines) - 1
    # ["*   ", "+  ", ... ]
    operators = re.findall(r"[\*\+]\s*", lines[-1])
    # pad last operator to avoid off-by-one error
    operators[-1] += " "
    for operator in operators:
        # how wide is this equation
        op_length = len(operator)
        operands = []
        # get all operands from each row, preserving whitespace
        for j in range(num_operands):
            num = lines[j][: op_length - 1]
            operands.append(num)
            # chop off the start of the line
            lines[j] = lines[j][op_length:]
        operator = operator[:1]
        # aggregate the operands normally for part 1
        part_one += OP_MAP[operator](map(lambda x: int(x.strip()), operands))
        operands_two = []
        # transpose the operands for part 2, then aggregate
        for j in range(op_length - 1):
            s = ""
            for row in operands:
                s += row[j].strip()
            operands_two.append(int(s))
        part_two += OP_MAP[operator](operands_two)

    return part_one, part_two


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{part_one=}, {part_two=} ({time_us}µs)")
