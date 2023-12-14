import sys
from time import perf_counter


class Grid:
    def __init__(self, lines: list[str]):
        self._grid = [list(line) for line in lines]
        self.width = len(self._grid[0])
        self.height = len(self._grid)
        self.stones = []
        for y, row in enumerate(self._grid):
            for x, char in enumerate(row):
                if char == "O":
                    self.stones.append((x, y))
        self.num_stones = len(self.stones)

    def print(self, highlight: tuple[int, int] | None = None):
        rep = []
        if highlight is None:
            highlight = (-1, -1)
        for y, row in enumerate(self._grid):
            for x, char in enumerate(row):
                if (x, y) == highlight:
                    rep.append("@")
                else:
                    rep.append(char)
            rep.append("\n")
        print("".join(rep))

    def shift(self, horizontal: bool, negative: bool) -> bool:
        moved = 0
        self.stones = sorted(
            self.stones, key=lambda x: x[~horizontal], reverse=not negative
        )
        for i in range(self.num_stones):
            stone = self.stones[i]
            new_stone = self.shift_stone(stone, horizontal, negative)
            if stone != new_stone:
                moved += 1
            self.stones[i] = new_stone

        return moved > 0

    def spin_cycle(self, full: bool = True) -> bool:
        movement = False
        if full:
            movement = movement or self.shift(False, True)  # N
        movement = movement or self.shift(True, True)  # W
        movement = movement or self.shift(False, False)  # S
        movement = movement or self.shift(True, False)  # E
        return movement

    def shift_stone(
        self, stone: tuple[int, int], horizontal: bool, negative: bool
    ) -> tuple[int, int]:
        sx, sy = stone
        delta = -1 if negative else 1
        dx = delta if horizontal else 0
        dy = delta if not horizontal else 0
        while (0 <= sx + dx < self.width) and (0 <= sy + dy < self.height):
            old_sx = sx
            old_sy = sy
            sx = sx + dx
            sy = sy + dy
            if self._grid[sy][sx] == ".":
                self._grid[sy][sx] = "O"
                self._grid[old_sy][old_sx] = "."
            else:
                sx = old_sx
                sy = old_sy
                break
        return (sx, sy)

    def north_load(self) -> int:
        total = 0
        for y, row in enumerate(self._grid):
            total += row.count("O") * (self.height - y)
        return total


def solve(lines: list[str]) -> tuple[int, int]:
    grid = Grid(lines)
    grid.shift(horizontal=False, negative=True)
    north_load = grid.north_load()
    # grid.spin_cycle(full=False)
    # for i in range(1000000000 - 1):
    #     check = i % 100000 == 0
    #     if check:
    #         print(f"{i=}")
    #     moving = grid.spin_cycle()
    #     if not moving:
    #         break
    north_load_spun = grid.north_load()
    return north_load, north_load_spun


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    north_load, north_load_spun = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{north_load=}, {north_load_spun=} ({time_us}ms)")
