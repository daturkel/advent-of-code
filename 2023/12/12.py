import re
import sys
from itertools import combinations
from time import perf_counter


def solve(lines: list[str]) -> tuple[int, int]:
    pattern = re.compile("#+")
    arrangement_sum = 0
    for line in lines:
        row, numbers = line.split(" ")
        numbers = [int(num) for num in numbers.split(",")]
        q_indices = [i for i, char in enumerate(row) if char == "?"]
        num_missing_qs = sum(numbers) - row.count("#")
        solutions_dict = {}
        for combo in combinations(q_indices, num_missing_qs):
            temp = solutions_dict
            for key in combo[:-1]:
                temp = temp.setdefault(key, {})
            temp[combo[-1]] = None

        for new_q_indices in combinations(q_indices, num_missing_qs):
            row_version = "".join(
                ["#" if i in new_q_indices else char for i, char in enumerate(row)]
            )
            blocks = pattern.findall(row_version)
            if [len(block) for block in blocks] == numbers:
                arrangement_sum += 1

    return arrangement_sum, 0


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    arrangement_sum, num_inside = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{arrangement_sum=}, {num_inside=} ({time_us}ms)")
