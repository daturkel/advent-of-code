import sys
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
    changes = {i: [] for i in range(len(lines))}
    digits = {i: [] for i in range(len(lines))}
    prices = {i: {} for i in range(len(lines))}
    all_combos_seen = set()
    for i, line in enumerate(lines):
        n = int(line)
        first_digit_old = n % 10
        for _ in range(2000):
            digits[i].append(first_digit_old)
            tmp = step_three(step_two(step_one(n)))
            first_digit_new = tmp % 10
            changes[i].append(first_digit_new - first_digit_old)
            first_digit_old = first_digit_new
            n = tmp
        digits[i].append(first_digit_old)
        part_one += n
        combos_seen = set()
        for j in range(len(changes[i])):
            if j < 3:
                continue
            combo = (
                changes[i][j - 3],
                changes[i][j - 2],
                changes[i][j - 1],
                changes[i][j],
            )
            if combo in combos_seen:
                continue
            else:
                combos_seen.add(combo)
                prices[i][combo] = digits[i][j + 1]
        all_combos_seen = all_combos_seen.union(combos_seen)

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
