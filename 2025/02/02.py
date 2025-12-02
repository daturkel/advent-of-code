import sys
from itertools import batched
from time import perf_counter


def solve(data: str) -> tuple[int, int]:
    part_one = 0
    part_two = 0
    for pair in data.split(","):
        lo, hi = pair.split("-")
        lo = int(lo)
        hi = int(hi)
        for i in range(lo, hi + 1):
            stri = str(i)
            length = len(stri)
            if length == 1:
                continue
            if length % 2 == 0 and len(set(batched(stri, length // 2))) == 1:
                part_one += i
                part_two += i
            # one character repeating
            elif len(set(stri)) == 1:
                part_two += i
            elif length % 3 == 0 and len(set(batched(stri, length // 3))) == 1:
                part_two += i
            elif length % 5 == 0 and len(set(batched(stri, length // 5))) == 1:
                part_two += i

    return part_one, part_two


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
