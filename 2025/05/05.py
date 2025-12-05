import sys
from time import perf_counter


def combine_ranges(a: range, b: range) -> range | None:
    """Combine two ranges into one if possible, else return None"""
    if a.start <= b.start and a.stop >= b.stop:
        return a
    elif b.start <= a.start and b.stop >= a.stop:
        return b
    elif a.stop >= b.start and a.start <= b.start:
        return range(a.start, b.stop)
    elif b.stop >= a.start and b.start <= a.start:
        return range(b.start, a.stop)
    return None


def consolidate_ranges(ranges: list[range]) -> tuple[list[range], int]:
    """Make one pass attempting to combine all ranges in a list and return the new list as well
    as the sum of all range lengths."""
    length = 0
    new_ranges = []
    while ranges:
        new_range = ranges.pop()
        to_remove = []
        for i in range(len(ranges)):
            combined = combine_ranges(new_range, ranges[i])
            if combined:
                new_range = combined
                to_remove.append(i)
        new_ranges.append(new_range)
        length += len(new_range)
        for index in reversed(to_remove):
            ranges.pop(index)
    return new_ranges, length


def solve(lines: list[str]) -> tuple[int, int]:
    part_one = 0

    # Build up list of ranges
    ranges = []
    for i, line in enumerate(lines):
        if line == "":
            break
        lo, hi = line.split("-", 1)
        lo = int(lo)
        hi = int(hi)
        ranges.append(range(lo, hi + 1))

    # Check which numbers are in a range
    for line in lines[i + 1 :]:
        for range_ in ranges:
            if int(line) in range_:
                part_one += 1
                break

    # Consolidate ranges until it's stable
    ranges, length = consolidate_ranges(ranges)
    while True:
        new_ranges, new_length = consolidate_ranges(ranges)
        if length == new_length:
            break
        ranges = new_ranges
        length = new_length

    return part_one, length


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
