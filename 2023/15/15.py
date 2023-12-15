import sys
from collections import defaultdict
from time import perf_counter


def hash_algo(s: str) -> int:
    current_value = 0
    for char in s:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value


def solve(steps: list[str]) -> tuple[int, int]:
    initialization_total = 0
    boxes = defaultdict(dict)
    for step in steps:
        initialization_total += hash_algo(step)
        if "=" in step:
            label, focal_length = step.split("=")
            focal_length = int(focal_length)
            box = boxes[hash_algo(label)]
            box[label] = focal_length
        else:
            label = step[:-1]
            box = boxes[hash_algo(label)]
            if label in box:
                del box[label]

    focusing_power = 0
    for box_num, box in boxes.items():
        for i, focal_length in enumerate(box.values()):
            focusing_power += (box_num + 1) * (i + 1) * focal_length

    return initialization_total, focusing_power


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        steps = file.read().split(",")

    initialization, focusing_power = solve(steps)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(hash_algo("qp"))
    print(f"{initialization=}, {focusing_power=} ({time_us}ms)")
