import sys
from time import perf_counter


def add_missing_numbers(numbers: set[int], map_: dict[int, int]) -> dict[int, int]:
    for number in numbers:
        if number not in map_:
            map_[number] = number
    return map_


def get_location(lines: list[str]) -> int:
    seeds = [int(seed) for seed in lines[0][7:].split()]
    current_numbers = set(seeds)
    maps = [{}]
    map_idx = 0
    for line in lines[3:]:
        if line == "":
            continue
        elif "map" in line:
            maps[map_idx] = add_missing_numbers(current_numbers, maps[map_idx])
            current_numbers = set(maps[map_idx].values())
            map_idx += 1
            maps.append({})
        else:
            dest_start, source_start, length = [int(num) for num in line.split()]
            for number in current_numbers:
                if source_start <= number <= source_start + length - 1:
                    diff = number - source_start
                    maps[map_idx][source_start + diff] = dest_start + diff
    # finish up the last mapping
    else:
        maps[map_idx] = add_missing_numbers(current_numbers, maps[map_idx])

    return min(maps[map_idx].values())


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    location = get_location(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{location=} ({time_us}µs)")
