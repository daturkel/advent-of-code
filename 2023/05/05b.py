import sys
from time import perf_counter

intvl = tuple[int, int]


def interval_setminus(this_intvl: intvl, subtract_intvls: list[intvl]) -> list[intvl]:
    """Take an interval and perform a setminus to remove all of the subtract_intvls from
    it, returning a list of intervals needed to represent the result.

    E.g. this_intvl = (0,10), subtract_intvls = [(2,3), (4,6), (10,12)]
    -> [(0,1), (7,9)] (the intervals remaining after subtracting subtract_intvls from this_intvl)
    """
    # copy the list so we don't modify it
    subtract_intvls = [intvl for intvl in subtract_intvls]
    # this will hold all the subintervals remaining after subtracting each of the "subtract_intvls"
    new_intvls = set([this_intvl])
    while subtract_intvls:
        s_intvl = subtract_intvls.pop()
        old_intvls = list(new_intvls)
        new_intvls = set()
        while old_intvls:
            this_intvl = old_intvls.pop()
            _, diffs = get_overlap_and_diffs(s_intvl, this_intvl)
            # not sure whether there might be duplicates, so using a set just in case
            # it doesn't seem to impact performance either way
            new_intvls.update(diffs)

    return list(new_intvls)


def add_missing_intervals(
    intvls: set[intvl], map_: dict[intvl, intvl]
) -> dict[intvl, intvl]:
    """The map `map_` maps a source interval to a destination interval. However, any unmapped
    intervals OR SUBSETS OF UNMAPPED INTERVALS from the last round must be mapped to themselves.
    We use interval_setminus to find the subitnervals of any intervals to map to themselves.
    """
    for intvl in intvls:
        for intvl_to_add in interval_setminus(intvl, list(map_.keys())):
            map_[intvl_to_add] = intvl_to_add

    return map_


def get_overlap_and_diffs(a: intvl, b: intvl) -> tuple[intvl | None, list[intvl]]:
    """Return the overlap between a and b, and the difference a setminus b. The difference
    is always represented as a list of 0 or more intervals (inclusive ranges)."""
    # a b B A
    if a[0] <= b[0] and a[1] >= b[1]:
        overlap = b
        diffs = [(a[0], b[0] - 1), (b[1] + 1, a[1])]
    # b a A b
    elif b[0] <= a[0] and b[1] >= a[1]:
        overlap = a
        diffs = [(b[0], a[0] - 1), (a[1] + 1, b[1])]
    # a b A B
    elif a[0] <= b[0] and b[1] >= a[1] > b[0]:
        overlap = (b[0], a[1])
        diffs = [(a[1] + 1, b[1])]
    # b a B A
    elif b[0] <= a[0] and a[1] >= b[1] > a[0]:
        overlap = (a[0], b[1])
        diffs = [(b[1] + 1, a[1])]
    else:
        overlap = None
        diffs = [b]
    # remove any diffs where the end is less than the start
    diffs = [diff for diff in diffs if diff[0] <= diff[1]]
    return overlap, diffs


def get_location(lines: list[str]) -> int:
    seeds_raw = [int(seed) for seed in lines[0][7:].split()]
    seeds = [
        (seeds_raw[i], seeds_raw[i] + seeds_raw[i + 1] - 1)
        for i in range(0, len(seeds_raw), 2)
    ]
    current_intvls = set(seeds)
    maps = [{}]
    map_idx = 0
    for line in lines[3:]:
        if line == "":
            continue
        elif "map" in line:
            maps[map_idx] = add_missing_intervals(current_intvls, maps[map_idx])
            current_intvls = set(maps[map_idx].values())
            map_idx += 1
            maps.append({})
        else:
            dest_start, source_start, length = [int(num) for num in line.split()]
            for intvl in current_intvls:
                overlap, _ = get_overlap_and_diffs(
                    intvl, (source_start, source_start + length - 1)
                )
                if overlap is not None:
                    diff = overlap[0] - source_start
                    overlap_length = overlap[1] - overlap[0]
                    maps[map_idx][overlap] = (
                        dest_start + diff,
                        dest_start + diff + overlap_length,
                    )
    # finish up the last mapping
    else:
        maps[map_idx] = add_missing_intervals(current_intvls, maps[map_idx])

    return min(maps[map_idx].values())[0]


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    location = get_location(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{location=} ({time_us}ms)")
