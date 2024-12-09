import sys
from copy import copy
from dataclasses import dataclass
from time import perf_counter

MaybeInt = int | None


@dataclass
class ContEmpty:
    idx: int
    length: int


@dataclass
class ContData:
    id: int
    idx: int
    length: int


def parse_disk(
    data: str,
) -> tuple[list[MaybeInt], list[int], list[ContData], list[ContEmpty]]:
    nums = [int(c) for c in data]
    disk: list[int | None] = [None] * sum(nums)
    id_num = 0
    idx = 0
    empties = []
    contiguous_empties = []
    contiguous_data = []
    # build up disk
    for i, n in enumerate(nums):
        if i % 2 == 0:
            disk[idx : idx + n] = [id_num] * n
            contiguous_data = [ContData(id_num, idx, n)] + contiguous_data
            id_num += 1
        else:
            empties = list(range(idx + n - 1, idx - 1, -1)) + empties
            contiguous_empties.append(ContEmpty(idx, n))
        idx += n
    return disk, empties, contiguous_data, contiguous_empties


def get_checksum(disk: list[MaybeInt]) -> int:
    checksum = 0
    for i, d in enumerate(disk):
        d = 0 if d is None else d
        checksum += i * d
    return checksum


def solve_a(disk: list[MaybeInt], empties: list[int]) -> int:
    # compact disk
    next_id = None
    while empties:
        empty_idx = empties.pop()
        while next_id is None:
            next_id = disk.pop()
        try:
            disk[empty_idx] = next_id
        except IndexError:
            disk.append(next_id)
            break
        next_id = None

    return get_checksum(disk)


def solve_b(
    disk: list[MaybeInt],
    contiguous_data: list[ContData],
    contiguous_empties: list[ContEmpty],
) -> int:
    for block in contiguous_data:
        for empty in contiguous_empties:
            # if there's space
            if block.length <= empty.length:
                # move data
                disk[empty.idx : empty.idx + block.length] = [block.id] * block.length
                # empty old position
                disk[block.idx : block.idx + block.length] = [None] * block.length
                # modify empty space
                empty.length -= block.length
                empty.idx += block.length
                break
            # don't move data to the right of its current position
            elif empty.idx > block.idx:
                break

    return get_checksum(disk)


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        data = file.read().strip()

    disk, empties, contiguous_data, contiguous_empties = parse_disk(data)
    part_one = solve_a(copy(disk), empties)
    part_two = solve_b(disk, contiguous_data, contiguous_empties)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
