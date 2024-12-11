import sys
from time import perf_counter


def solve(stones_str: str) -> tuple[int, int]:
    stones = [int(n) for n in stones_str.split()]
    for _ in range(25):
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                str_stone = str(stone)
                left = int(str_stone[: len(str_stone) // 2])
                right = int(str_stone[len(str_stone) // 2 :])
                new_stones += [left, right]
            else:
                new_stones.append(stone * 2024)
        stones = new_stones
        print(len(stones))
        input()
    return len(stones), 0


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        stones = file.read().strip()

    part_one, part_two = solve("0")
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
