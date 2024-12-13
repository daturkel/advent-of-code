import re
import sys
from dataclasses import dataclass
from time import perf_counter

NUMBER_PATTERN = re.compile(r"\d+")


@dataclass
class Game:
    ax: int
    ay: int
    bx: int
    by: int
    px: int
    py: int

    def solve(self) -> tuple[int, int]:
        denominator = self.ax * self.by - self.ay * self.bx
        numerator_a = self.px * self.by - self.py * self.bx
        numerator_b = self.ax * self.py - self.px * self.ay

        # Cramer's Rule
        a = numerator_a / denominator
        b = numerator_b / denominator
        if a.is_integer() and b.is_integer():
            return int(a), int(b)
        else:
            return 0, 0


def solve(lines: list[str]) -> tuple[int, int]:
    games: list[Game] = []
    ax, ay, bx, by, px, py = 0, 0, 0, 0, 0, 0
    for line in lines:
        if line == "\n":
            continue
        n1, n2 = NUMBER_PATTERN.findall(line)
        if line.startswith("Button A"):
            ax, ay = int(n1), int(n2)
        elif line.startswith("Button B"):
            bx, by = int(n1), int(n2)
        else:
            px, py = int(n1), int(n2)
            games.append(Game(ax, ay, bx, by, px, py))

    cost_one = 0
    cost_two = 0
    for game in games:
        a, b = game.solve()
        cost_one += 3 * a + b
        game.px += 10000000000000
        game.py += 10000000000000
        a, b = game.solve()
        cost_two += 3 * a + b
    return cost_one, cost_two


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.readlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{part_one=}, {part_two=} ({time_us}µs)")
