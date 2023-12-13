import re
import sys
from collections.abc import Sequence
from itertools import combinations
from time import perf_counter


class BranchingDict:
    def __init__(self):
        self.dict = {}

    def add(self, path: Sequence[int]):
        temp = self.dict
        for key in path[:-1]:
            temp = temp.setdefault(key, {})
        try:
            temp[path[-1]] = None
        except IndexError:
            print(path)
            exit()

    def get(self, path: Sequence[int]) -> dict | None:
        value = self.dict
        for key in path:
            value = value[key]
        return value

    def prune(self, path: Sequence[int]):
        if len(path) == 1:
            del self.dict[path[0]]
            return
        parent = self.get(path[:-1])
        del parent[path[-1]]  # type: ignore
        if parent == {}:
            self.prune(path[:-1])

    def get_a_path(self) -> list[int]:
        temp = self.dict
        path = []
        while temp is not None:
            key = list(temp.keys())[0]
            path.append(key)
            temp = temp[key]
        return path


def solve_line(line: str, multiplier: int, pattern: re.Pattern) -> int:
    row, numbers = line.split(" ")
    numbers = [int(num) for num in numbers.split(",")]
    row = row * multiplier
    numbers = numbers * multiplier
    q_indices = [i for i, char in enumerate(row) if char == "?"]
    num_missing_qs = sum(numbers) - row.count("#")
    solution_tree = BranchingDict()
    if num_missing_qs == 0:
        return 1
    print(len(q_indices))
    print(num_missing_qs)
    for combo in combinations(q_indices, num_missing_qs):
        solution_tree.add(combo)

    arrangements = 0

    while solution_tree.dict:
        row_as_list = list(row)
        path = solution_tree.get_a_path()
        remaining_q_indices = [q for q in q_indices]
        valid_prefix = True
        string_so_far = ""
        blocks = []
        # check for early stopping
        for path_idx in range(len(path)):
            row_idx = path[path_idx]
            row_as_list[row_idx] = "#"
            remaining_q_indices.remove(row_idx)
            for q_index in [i for i in remaining_q_indices if i < row_idx]:
                row_as_list[q_index] = "."
            string_so_far = "".join(row_as_list).split("?")[0]
            blocks = [len(block) for block in pattern.findall(string_so_far)]
            first_blocks = blocks[:-1]
            last_block = blocks[-1]

            if (
                (first_blocks != numbers[: len(first_blocks)])
                or (len(numbers) < len(blocks))
                or (last_block > numbers[len(blocks) - 1])
            ):
                solution_tree.prune(path[: path_idx + 1])
                valid_prefix = False
                break
        if valid_prefix:
            final_blocks = [
                len(block) for block in pattern.findall("".join(row_as_list))
            ]
            if final_blocks == numbers:
                arrangements += 1
            solution_tree.prune(path)

    return arrangements


def solve(lines: list[str]) -> tuple[int, int]:
    pattern = re.compile("#+")
    arrangement_list_a = []
    arrangement_list_b = []
    for line in lines:
        arrangements_a = solve_line(line, 1, pattern)
        arrangement_list_a.append(arrangements_a)

        arrangements_b = solve_line(line, 5, pattern)
        arrangement_list_b.append(arrangements_b)

    return sum(arrangement_list_a), sum(arrangement_list_b)


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    arrangement_sum, num_inside = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{arrangement_sum=}, {num_inside=} ({time_us}ms)")
