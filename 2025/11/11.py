import sys
from time import perf_counter

START = "you"
END = "out"

SERVER = "svr"
REQUIRED = ["dac", "fft"]


def solve(lines: list[str]) -> tuple[int, int]:
    part_one = 0
    part_two = 0
    graph = {}
    for line in lines:
        head, tail = line.split(": ")
        neighbors = tail.split(" ")
        graph[head] = neighbors
    stack = [START]
    explored = set()
    while stack:
        node = stack.pop()
        if node not in explored or True:
            explored.add(node)
            for edge in graph[node]:
                if edge == END:
                    part_one += 1
                else:
                    stack.append(edge)

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
