import sys
from time import perf_counter

pair = tuple[int, int]


def split_pair(this_pair: pair, subtract_pairs: list[pair]) -> list[pair]:
    subtract_pairs = [pair for pair in subtract_pairs]
    new_pairs = set([this_pair])
    while subtract_pairs:
        s_pair = subtract_pairs.pop()
        old_pairs = list(new_pairs)
        new_pairs = set()
        while old_pairs:
            this_pair = old_pairs.pop()
            _, diffs = get_overlap_and_diffs(s_pair, this_pair)
            new_pairs.update(diffs)

    return list(new_pairs)


def add_missing_numbers(pairs: set[pair], map_: dict[pair, pair]) -> dict[pair, pair]:
    for pair in pairs:
        for pair_to_add in split_pair(pair, list(map_.keys())):
            map_[pair_to_add] = pair_to_add

    return map_


def get_overlap_and_diffs(a: pair, b: pair) -> tuple[pair | None, list[pair]]:
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
    diffs = [diff for diff in diffs if diff[0] <= diff[1]]
    return overlap, diffs


def get_location(lines: list[str]) -> int:
    seeds_raw = [int(seed) for seed in lines[0][7:].split()]
    seeds = [
        (seeds_raw[i], seeds_raw[i] + seeds_raw[i + 1] - 1)
        for i in range(0, len(seeds_raw), 2)
    ]
    current_pairs = set(seeds)
    maps = [{}]
    map_idx = 0
    for line in lines[3:]:
        if line == "":
            continue
        elif "map" in line:
            maps[map_idx] = add_missing_numbers(current_pairs, maps[map_idx])
            current_pairs = set(maps[map_idx].values())
            map_idx += 1
            maps.append({})
        else:
            dest_start, source_start, length = [int(num) for num in line.split()]
            for pair in current_pairs:
                overlap, _ = get_overlap_and_diffs(
                    pair, (source_start, source_start + length - 1)
                )
                if overlap is not None:
                    diff = overlap[0] - source_start
                    overlap_length = overlap[1] - overlap[0]
                    maps[map_idx][overlap] = (
                        dest_start + diff,
                        dest_start + diff + overlap_length,
                    )
    else:
        maps[map_idx] = add_missing_numbers(current_pairs, maps[map_idx])

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
