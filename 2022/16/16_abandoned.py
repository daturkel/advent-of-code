#!/usr/bin/env python3

import re
import sys
from time import perf_counter

Valve = tuple[int, bool, list[str]]
Path = list[str]


def parse_input(lines: list[str]) -> tuple[dict[str, Valve], list[str]]:
    valves: dict[str, Valve] = {}
    nonzero_valves = []
    pattern = re.compile(r"Valve (..).*?(\d+).*valves? (.*)")
    for line in lines:
        this_valve, flow_str, next_valves_str = pattern.findall(line)[0]
        flow = int(flow_str)
        next_valves = next_valves_str.split(", ")
        valves[this_valve] = (flow, False, next_valves)
        if flow:
            nonzero_valves.append(this_valve)

    return valves, nonzero_valves


def fastest_paths(
    valves: dict[str, Valve],
    a: str,
    b: str,
    visited: list | None = None,
) -> list[str]:
    print(a)
    print(visited)
    print()
    if visited is None:
        visited = [a]

    options = [valve for valve in valves[a][2] if valve not in visited]

    if b in options:
        return [visited + [b]]

    paths = [fastest_paths(valves, option, b, visited + [option]) for option in options]
    min_path = 1e5
    shortest_paths = []
    for path in paths:
        if not path:
            continue
        length = len(path[0])
        if length < min_path:
            min_path = length
            shortest_paths =path
        elif length == min_path:
            shortest_paths.append(path)


    return shortest_paths


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = [line.rstrip() for line in file.readlines()]

    tic = perf_counter()
    valves, nonzero_valves = parse_input(lines)
    print(fastest_paths(valves, "AA", "JJ"))

    result = 0
    toc = perf_counter()
    time_us = round((toc - tic), 1)

    print(f"{result=} ({time_us}s)")
