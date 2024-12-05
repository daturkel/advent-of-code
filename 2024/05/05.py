import sys
from collections import defaultdict
from functools import cmp_to_key
from time import perf_counter


def solve(lines: list[str]) -> tuple[int, int]:
    followers = defaultdict(set)
    correct_centers = 0
    fixed_centers = 0
    for i, line in enumerate(lines):
        if line == "\n":
            break
        left = int(line[:2])
        right = int(line[3:])
        followers[left].add(right)
    # used for part 2; defined here so it's not redefined in every loop
    compare = cmp_to_key(lambda x, y: 1 if x in followers[y] else -1)
    for line in lines[i + 1 :]:
        pages = [int(n) for n in line.strip().split(",")]
        valid = True
        added = set()
        for page in pages[::-1]:
            # part 1
            if added.issubset(followers[page]):
                added.add(page)
            else:
                valid = False
                break
        if valid:
            correct_centers += pages[len(pages) // 2]
        else:
            # part 2
            # manual insertion sort
            # new_order = []
            # while pages:
            #     to_sort = pages.pop()
            #     for i, page in enumerate(new_order):
            #         if page not in followers[to_sort]:
            #             break
            #     else:
            #         # if we ran out of pages, we will add to the very end, which means
            #         # incrementing the insertion index once more
            #         i += 1
            #     new_order.insert(i, to_sort)
            new_order = sorted(pages, key=compare)
            fixed_centers += new_order[len(new_order) // 2]

    return correct_centers, fixed_centers


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.readlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{part_one=}, {part_two=} ({time_us}µs)")
