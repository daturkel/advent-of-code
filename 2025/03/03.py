import sys
from time import perf_counter


def first_highest(nums: list[int]) -> tuple[int, list[int]]:
    """Get the highest digit in a list and return the numbers after its first instance"""
    highest = max(nums)
    index = nums.index(highest)
    remaining = nums[index + 1 :]
    return highest, remaining


def highest_n_digits(n, nums: list[int]) -> int:
    """Iteratively call first_highest, leaving a shrinking margin off the right side to
    ensure we're able to produce enough digits."""
    digits = []
    remaining = nums
    for i in range(n - 1, -1, -1):
        if i == 0:
            to_check = remaining
        else:
            to_check = remaining[:-i]
        digit, remaining = first_highest(to_check)
        digits.append(digit)
        remaining += nums[-i:]  # add back the part we reserved
    return int("".join(str(d) for d in digits))


def solve(lines: list[str]) -> tuple[int, int]:
    part_one = 0
    part_two = 0

    for line in lines:
        nums = [int(c) for c in line]
        part_one += highest_n_digits(2, nums)
        part_two += highest_n_digits(12, nums)

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
