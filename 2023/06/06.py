import sys
from time import perf_counter


def get_num_solutions(time: int, record: int) -> int:
    """We want to know how many integral solutions there are to
    (time - charge)*charge ≥ record
    So we count the number of integers between the roots of the rewritten quadratic equation:
    -1 * charge^2 + time * charge - record = 0"""
    a = -1
    b = time
    c = -1 * record
    neg_b = -1 * b
    discriminant = (b**2 - 4 * a * c) ** (0.5)
    denominator = 2 * a
    root_1 = (neg_b + discriminant) / denominator
    root_2 = (neg_b - discriminant) / denominator
    # round up for the lower root
    if root_1 != int(root_1):
        root_1 = int(root_1 + 1)
    # round down for the higher root
    root_2 = int(root_2)
    # return number of solutions
    return root_2 - root_1 + 1


def get_ways_to_win(lines: list[str]) -> tuple[int, int]:
    times = [int(num) for num in lines[0].split()[1:]]
    records = [int(num) for num in lines[1].split()[1:]]

    total_a = 1
    for time, record in zip(times, records):
        ways_to_win = 0
        for charge in range(1, time):
            time_left = time - charge
            dist_achieved = charge * time_left
            if dist_achieved > record:
                ways_to_win += 1
        total_a *= ways_to_win

    new_time = int("".join(str(num) for num in times))
    new_record = int("".join(str(num) for num in records))
    new_ways_to_win = 0

    new_ways_to_win = get_num_solutions(new_time, new_record)

    return total_a, new_ways_to_win


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    ways_to_win, num_cards = get_ways_to_win(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{ways_to_win=}, {num_cards=} ({time_us}µs)")
