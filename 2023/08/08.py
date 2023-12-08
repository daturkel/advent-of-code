import sys
from math import lcm
from time import perf_counter


def get_steps_til_end(
    start: str, directions: list[int], graph: dict[str, tuple[str, str]]
) -> int:
    current_node = start
    n_directions = len(directions)
    num_steps = 0
    while current_node[2] != "Z":
        num_steps += 1
        direction = directions[(num_steps - 1) % n_directions]
        current_node = graph[current_node][direction]
    return num_steps


def solve(lines: list[str]) -> tuple[int, int]:
    directions = [{"L": 0, "R": 1}[direction] for direction in lines[0]]
    graph = {}
    for line in lines[2:]:
        node = line[:3]
        left = line[7:10]
        right = line[12:15]
        graph[node] = [left, right]

    starts = [node for node in graph.keys() if node[2] == "A"]
    cycle_lengths = []
    num_steps_a = 0
    for start in starts:
        length = get_steps_til_end(start, directions, graph)
        cycle_lengths.append(length)
        if start == "AAA":
            num_steps_a = length

    num_steps_b = lcm(*cycle_lengths)

    return num_steps_a, num_steps_b


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    num_steps, alt_num_steps = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{num_steps=}, {alt_num_steps=} ({time_us}ms)")
