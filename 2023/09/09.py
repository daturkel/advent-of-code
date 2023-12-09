import sys
from time import perf_counter


def solve(lines: list[str]) -> tuple[int, int]:
    total_forward = 0
    total_backward = 0

    for line in lines:
        line = [int(num) for num in line.split()]
        buffer = []
        current = line
        # build up differences
        while True:
            differences = [current[i + 1] - current[i] for i in range(len(current) - 1)]
            if set(differences) == {0}:
                break
            buffer.append(differences)
            current = differences
        # extrapolate differences backwards and forwards
        diff_forward = 0
        diff_backward = 0
        while buffer:
            this_buffer = buffer.pop()  # read list of differences backwards
            this_buffer = (
                [this_buffer[0] - diff_backward]  # extrapolate backwards
                + this_buffer
                + [this_buffer[-1] + diff_forward]  # extrapolate forwards
            )
            diff_forward = this_buffer[-1]
            diff_backward = this_buffer[0]
        total_forward += line[-1] + diff_forward
        total_backward += line[0] - diff_backward

    return total_forward, total_backward


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    forward, backward = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{forward=}, {backward=} ({time_us}ms)")
