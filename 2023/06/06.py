import sys
from time import perf_counter


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
    for charge in range(1, new_time):
        time_left = new_time - charge
        dist_achieved = charge * time_left
        if dist_achieved > new_record:
            new_ways_to_win += 1

    return total_a, new_ways_to_win


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    ways_to_win, num_cards = get_ways_to_win(lines)
    toc = perf_counter()
    time_us = round((toc - tic), 1)

    print(f"{ways_to_win=}, {num_cards=} ({time_us}s)")
