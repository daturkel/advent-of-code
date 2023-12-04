import sys
from time import perf_counter


def get_possible_and_power(
    games: list[str], max_per_color: dict[str, int]
) -> tuple[int, int]:
    total_possible = 0
    total_power = 0
    for i, game in enumerate(games, start=1):
        game = game.split(": ", 1)[1]  # remove "Game N: " prefix
        valid_game = True
        color_min = {"red": 0, "blue": 0, "green": 0}
        for reveal in game.split("; "):  # split into rounds
            for color in reveal.split(", "):  # split into color-number pairs
                num, color = color.split(" ")  # split color from number
                num = int(num)
                if num > color_min[color]:
                    color_min[color] = num
                # don't bother re-checking against max if game is already invalid
                if valid_game and (num > max_per_color[color]):
                    valid_game = False
        if valid_game:
            total_possible += i  # assumption that game # is always sequential
        total_power += color_min["red"] * color_min["blue"] * color_min["green"]
    return total_possible, total_power


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    id_sum, power_sum = get_possible_and_power(
        lines, {"red": 12, "blue": 14, "green": 13}
    )
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{id_sum=}, {power_sum=} ({time_us}µs)")
