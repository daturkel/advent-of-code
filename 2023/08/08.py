import sys
from time import perf_counter


def get_steps(lines: list[str]) -> tuple[int, int]:
    directions = [{"L": 0, "R": 1}[direction] for direction in lines[0]]
    n_directions = len(directions)
    graph = {}
    for line in lines[2:]:
        node = line[:3]
        left = line[7:10]
        right = line[12:15]
        graph[node] = [left, right]

    num_steps = 0
    current_node = "AAA"
    visited = [current_node]
    while current_node != "ZZZ":
        num_steps += 1
        direction = directions[(num_steps - 1) % n_directions]
        current_node = graph[current_node][direction]
        visited.append(current_node)

    return num_steps, 0


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    num_steps, alt_winnings = get_steps(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{num_steps=}, {alt_winnings=} ({time_us}ms)")
