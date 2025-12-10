import sys
from itertools import combinations
from time import perf_counter

from pulp import GUROBI, LpInteger, LpProblem, LpVariable, value


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

        prob = LpProblem()
        variables = [
            LpVariable(f"x{i}", 0, None, LpInteger) for i in range(len(buttons))
        ]
        # minimize sum of button presses
        prob += sum(variables)
        # add constraints
        for ix, j in enumerate(joltages):
            prob += (
                sum(  # sum of
                    [
                        variables[bix]  # variable corresponding to this button
                        for bix, button in enumerate(buttons)
                        if ix in button  # if the corresponding light is on this button
                    ]
                )
                == j  # == total joltage
            )
        GUROBI(msg=0).solve(prob)  # type: ignore
        part_two += int(value(prob.objective))  # type: ignore

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
