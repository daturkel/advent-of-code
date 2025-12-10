import sys
from itertools import combinations
from time import perf_counter

import numpy as np


def solve(lines: list[str]) -> tuple[int, int]:
    part_one = 0
    part_two = 0
    all_lights = []
    all_buttons = []
    all_joltages = []
    for line in lines:
        this_lights_str, line = line.split(maxsplit=1)
        this_lights = [char == "#" for char in this_lights_str[1:-1]]
        all_lights.append(this_lights)
        this_buttons_str, this_joltages = line.rsplit(maxsplit=1)
        this_buttons = []
        for button_str in this_buttons_str.split(" "):
            button = [int(b) for b in button_str[1:-1].split(",")]
            this_buttons.append(button)
        all_buttons.append(this_buttons)
        all_joltages.append([int(j) for j in this_joltages[1:-1].split(",")])

    for ix in range(len(lines)):
        lights = all_lights[ix]
        joltages = all_joltages[ix]
        buttons = all_buttons[ix]
        solved = False
        for n_buttons in range(len(lights)):
            for button_set in combinations(buttons, n_buttons):
                light_trial = [False for _ in range(len(lights))]
                for button in button_set:
                    for n in button:
                        light_trial[n] = not light_trial[n]
                if light_trial == lights:
                    solved = True
                    part_one += n_buttons
                    break
            if solved:
                break
        solved = False
        A = [[0] * len(buttons) for _ in range(len(lights))]
        for i, button in enumerate(buttons):
            for n in button:
                A[n][i] = 1
        for row in A:
            print(row)
        print()
        print(joltages)
        print(np.linalg.lstsq(A, joltages))
        print()

    return part_one, part_two


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
