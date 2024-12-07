import sys
from itertools import product
from operator import add, mul
from time import perf_counter
from typing import Callable

PLUS = add
TIMES = mul
CAT = lambda x, y: x * 10 ** len(str(y)) + y  # noqa: E731


def get_operation_combinations(
    num_ops: int, cache: dict = {}
) -> list[tuple[Callable, ...]]:
    try:
        return cache[num_ops]
    except KeyError:
        # must be a list so that it doesn't get exhausted after one use like an iterable
        result = list(product([PLUS, TIMES, CAT], repeat=num_ops))
        cache[num_ops] = result
        return result


def solve(lines: list[str]) -> tuple[int, int]:
    part_one = 0
    part_two = 0
    for line in lines:
        test_value, nums = line.split(": ")
        test_value = int(test_value)
        nums = [int(num) for num in nums.split()]
        op_combos = get_operation_combinations(len(nums) - 1)
        for ops in op_combos:
            result = nums[0]
            for op, num in zip(ops, nums[1:]):
                result = op(result, num)
            if result == test_value:
                if CAT not in ops:
                    part_one += test_value
                part_two += test_value
                break

    return part_one, part_two


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.readlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
