#!/usr/bin/env python3

from collections import defaultdict
import sys
from time import perf_counter

Coord = tuple[int, int]
Piece = list[Coord]

# Coordinates relative to bottom left
PIECES = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
]


class Grid:
    def __init__(self, jets: list[int]):
        self.filled = set()
        self.top = -1
        self.jets = jets

    def piece_at_anchor(self, piece: Piece, anchor: Coord) -> Piece:
        new_piece = []
        for dx, dy in piece:
            new_piece.append((anchor[0] + dx, anchor[1] + dy))

        return new_piece

    def can_place(self, piece: Piece) -> bool:
        can_place = True
        for coord in piece:
            if (
                (coord[0] < 0)
                or (coord[0] >= 7)
                or (coord[1] < 0)
                or (coord in self.filled)
            ):
                can_place = False
                break

        return can_place

    def drop(self, piece: Piece, ji: int) -> int:
        anchor = (2, self.top + 4)
        piece_at_anchor = self.piece_at_anchor(piece, anchor)
        keep_falling = True
        while keep_falling:
            # shift jet
            jet = self.jets[ji % len(jets)]
            try_anchor = (anchor[0] + jet, anchor[1])
            try_piece_at_anchor = self.piece_at_anchor(piece, try_anchor)
            if self.can_place(try_piece_at_anchor):
                anchor = try_anchor
                piece_at_anchor = try_piece_at_anchor

            # fall
            try_anchor = (anchor[0], anchor[1] - 1)
            try_piece_at_anchor = self.piece_at_anchor(piece, try_anchor)
            if self.can_place(try_piece_at_anchor):
                anchor = try_anchor
                piece_at_anchor = try_piece_at_anchor
            else:
                keep_falling = False

            # increment jet index
            ji = ji + 1

        for coord in piece_at_anchor:
            self.filled.add(coord)

        self.top = max(coord[1] for coord in self.filled)

        return ji

    def show(self):
        output = [list(".......") for _ in range(self.top + 1)]
        for x, y in self.filled:
            output[y][x] = "#"

        for row in reversed(output):
            row_str = "".join(row)
            print(f"|{row_str}|")
        print("+-------+")
        print()


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        jets_str = file.read().rstrip()

    tic = perf_counter()
    jets = [1 if char == ">" else -1 for char in jets_str]
    grid = Grid(jets)
    ji = 0  # jet_index
    for pi in range(2022):  # piece index
        ji = grid.drop(PIECES[pi % len(PIECES)], ji)
        if pi < 5:
            grid.show()

    result = grid.top + 1  # (0-indexing)
    toc = perf_counter()
    time_us = round((toc - tic), 1)

    print(f"{result=} ({time_us}s)")
