from __future__ import annotations

import sys
from collections import defaultdict, deque
from time import perf_counter


class Node:
    def __init__(self):
        self.children: list[str] = []

    def add_parent(self, parent_name: str):
        pass

    def add_child(self, child: str):
        self.children.append(child)

    def pulse(self, high: bool, source: str) -> bool | None:
        return None


class Broadcaster(Node):
    def pulse(self, high: bool, source: str):
        return high


class FlipFlop(Node):
    def __init__(self):
        super().__init__()
        self.state = False

    def pulse(self, high: bool, source: str) -> bool | None:
        if high:
            return None
        else:
            self.state = not self.state
            return self.state


class Conjunction(Node):
    def __init__(self):
        super().__init__()
        self.memory = {}

    def add_parent(self, parent_name: str):
        self.memory[parent_name] = False

    def pulse(self, high: bool, source: str):
        self.memory[source] = high
        return not all(self.memory.values())


def get_name_and_type(raw_name: str) -> tuple[str, type[Node]]:
    if raw_name[0] == "%":
        return raw_name[1:], FlipFlop
    elif raw_name[0] == "&":
        return raw_name[1:], Conjunction
    elif raw_name == "broadcaster":
        return raw_name, Broadcaster
    else:
        return raw_name, Node


def solve(lines: list[str]) -> tuple[int, int]:
    nodes: dict[str, Node] = {}
    node_children_names = defaultdict(list)
    for line in lines:
        source, destinations = line.split(" -> ")
        name, node_type = get_name_and_type(source)
        if name not in nodes:
            nodes[name] = node_type()
        for destination in destinations.split(", "):
            node_children_names[name].append(destination)
    for parent, children in node_children_names.items():
        for child in children:
            if child not in nodes:
                nodes[child] = Node()
            nodes[parent].add_child(child)
            nodes[child].add_parent(parent)

    pulse_counter = {False: 0, True: 0}
    queue = deque()
    pulses_after_1000 = None
    presses_til_done = None
    i = 0
    while True:
        i += 1
        queue.append((False, "broadcaster", "button"))
        while queue:
            high, destination, source = queue.popleft()
            pulse_counter[high] += 1
            if (not high) and (destination == "rx") and (presses_til_done is None):
                print("ok")
                presses_til_done = i
                break
            result = nodes[destination].pulse(high, source)
            if result is not None:
                for child in nodes[destination].children:
                    queue.append((result, child, destination))
        if i == 1000:
            pulses_after_1000 = pulse_counter[False] * pulse_counter[True]
            print(pulses_after_1000)
        if presses_til_done:
            break

    return pulses_after_1000, presses_til_done  # type: ignore


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    pulses_after_1000, presses_til_done = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{pulses_after_1000=}, {presses_til_done=} ({time_us}µs)")
