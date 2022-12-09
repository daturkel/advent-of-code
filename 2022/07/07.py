#!/usr/bin/env python3

import sys
from time import perf_counter

CAPACITY = 70000000
REQUIRED = 30000000


class Node:
    def __init__(self, name: str, parent: "Node" | None, size: int | None = None):
        self.name = name
        self.parent = parent
        self._size = size
        self.children: dict[str, Node] = {}

    def get_size(self):
        if not self._size:
            self._size = sum(child.get_size() for child in self.children.values())
        return self._size


def find_folders(lines: list[str]) -> tuple[int, int]:
    folder_sizes = []
    root = Node(name="", parent=None)
    node = root

    for line in lines[1:]:
        match line.split():
            # go up
            case [_, "cd", ".."]:
                folder_sizes.append(node.get_size())
                node = node.parent # type: ignore
            # add a directory to filesystem
            case [_, "cd", dir_name]:
                node.children[dir_name] = Node(name=dir_name, parent=node)
                node = node.children[dir_name]
            # noop
            case [_, "ls"] | ["dir", _]:
                pass
            # add a file to filesystem
            case [size, name]:
                node.children[name] = Node(name=name, parent=node, size=int(size))

    # don't forget to add the last folder
    folder_sizes.append(node.get_size())
    # don't forget to add the root folder
    folder_sizes.append(root.get_size())

    # part a
    total_under_100k = sum([size for size in folder_sizes if size < 100000])

    # part b
    free = CAPACITY - folder_sizes[-1]
    need_to_delete = REQUIRED - free
    size_to_delete = min([size for size in folder_sizes if size > need_to_delete])
    return total_under_100k, size_to_delete


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = [line.rstrip("\n") for line in file.readlines()]

    tic = perf_counter()

    total_under_100k, size_to_delete = find_folders(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{total_under_100k=}, {size_to_delete=} ({time_us}µs)")
