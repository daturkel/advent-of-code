import sys
from time import perf_counter


def blink(stone: int, times: int, cache: dict[tuple[int, int], int] = {}) -> int:
    answer = 0
    if (stone, times) in cache:
        return cache[(stone, times)]
    elif times == 0:
        return 1
    elif stone == 0:
        answer = blink(1, times - 1)
    elif len(str(stone)) % 2 == 0:
        str_stone = str(stone)
        left = int(str_stone[: len(str_stone) // 2])
        right = int(str_stone[len(str_stone) // 2 :])
        answer = blink(left, times - 1) + blink(right, times - 1)
    else:
        answer = blink(2024 * stone, times - 1)
    cache[(stone, times)] = answer
    return answer


def solve(stones_str: str) -> tuple[int, int]:
    stones = [int(n) for n in stones_str.split()]
    part_one = 0
    part_two = 0
    for stone in stones:
        part_one += blink(stone, 25)
        part_two += blink(stone, 75)

    return part_one, part_two


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        stones = file.read().strip()

    part_one, part_two = solve(stones)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
