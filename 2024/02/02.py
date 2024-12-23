import sys
from time import perf_counter


def get_invalid_index(report: list[str]) -> tuple[bool, list[int]]:
    # first return value is whether this report is valid
    # second return value is an index which could make it valid if removed
    last = None
    sign = None
    for i, num in enumerate(report):
        num = int(num)
        if last is not None:
            diff = last - num
            if diff == 0:
                return False, [i]
            elif not (1 <= abs(diff) <= 3):
                return False, [i - 1, i]
            new_sign = diff > 0
            if (sign is not None) and (sign != new_sign):
                # i thought this should be [i-2, i-1, i], but [i-2, i] seems to work
                return False, [i - 2, i]
            sign = new_sign
        last = num
    return True, []


def solve(reports: list[str]) -> tuple[int, int]:
    safe = 0
    alt_safe = 0
    for report in reports:
        report = report.split()
        is_valid, index_to_remove = get_invalid_index(report)
        if is_valid:
            safe += 1
            alt_safe += 1
        elif index_to_remove is not None:
            for index in index_to_remove:
                new_report = report[:index] + report[index + 1 :]
                is_valid, _ = get_invalid_index(new_report)
                if is_valid:
                    alt_safe += 1
                    break

    return safe, alt_safe


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.readlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
