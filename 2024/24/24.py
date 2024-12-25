import sys
from operator import and_, or_, xor
from time import perf_counter
from typing import Callable


def solve(lines: list[str]) -> tuple[int, int]:
    values: dict[str, bool] = {}
    connections: list[tuple[Callable, str, str, str]] = []
    for i, line in enumerate(lines):
        if line == "":
            break
        name, value = line.split(": ", maxsplit=1)
        values[name] = bool(int(value))
    for line in lines[i + 1 :]:
        name1, op, name2, _, name3 = line.split(" ")
        op = {"AND": and_, "OR": or_, "XOR": xor}[op]
        connections.append((op, name1, name2, name3))

    i = 0
    part_one = 0
    while connections:
        i = i % len(connections)
        op, name1, name2, name3 = connections[i]
        if name1 in values and name2 in values:
            values[name3] = op(values[name1], values[name2])
            if name3.startswith("z"):
                z_num = int(name3[1:])
                part_one += int(values[name3]) * 2**z_num
            del connections[i]
        else:
            i = i + 1

    print(len(values))

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
