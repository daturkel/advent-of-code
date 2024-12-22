import sys
from collections import deque
from time import perf_counter


def step_one(n: int) -> int:
    tmp = n << 6
    n ^= tmp
    return n % (2**24)


def step_two(n: int) -> int:
    tmp = n >> 5
    n ^= tmp
    return n % (2**24)


def step_three(n: int) -> int:
    tmp = n << 11
    n ^= tmp
    return n % (2**24)


def solve(lines: list[str]) -> tuple[int, int]:
    part_one = 0
    prices = {i: {} for i in range(len(lines))}
    all_combos_seen = set()
    for i, line in enumerate(lines):
        buffer = deque([])
        n = int(line)
        first_digit_old = n % 10
        combos_seen = set()
        for _ in range(2000):
            tmp = step_three(step_two(step_one(n)))
            first_digit_new = tmp % 10
            buffer.append(first_digit_new - first_digit_old)
            if len(buffer) > 4:
                buffer.popleft()
                if tuple(buffer) not in combos_seen:
                    combos_seen.add(tuple(buffer))
                    prices[i][tuple(buffer)] = first_digit_new
            first_digit_old = first_digit_new
            n = tmp
        all_combos_seen = all_combos_seen.union(combos_seen)
        part_one += n

    most_bananas = 0
    for combo in all_combos_seen:
        bananas = 0
        for price_dict in prices.values():
            bananas += price_dict.get(combo, 0)
        most_bananas = max(bananas, most_bananas)
    return part_one, most_bananas


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
