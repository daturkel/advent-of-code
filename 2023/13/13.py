import sys
from time import perf_counter

import numpy as np
import numpy.typing as npt


def find_folds(matrix: npt.NDArray) -> tuple[int | None, int | None]:
    width = matrix.shape[1]
    pivot_a = None
    pivot_b = None
    for pivot in range(1, width):
        fold_size = min(pivot, width - pivot)
        left = matrix[:, pivot - fold_size : pivot]
        right = np.flip(matrix[:, pivot : pivot + fold_size], axis=1)
        num_different = (left != right).sum()
        if num_different == 0:
            pivot_a = pivot
        elif num_different == 1:
            pivot_b = pivot
        if (pivot_a is not None) and (pivot_b is not None):
            break
    return pivot_a, pivot_b


def solve(lines: list[str]) -> tuple[int, int]:
    total_a = 0
    total_b = 0
    buffer = []
    for line in lines + [""]:
        if line != "":
            buffer.append([0 if char == "#" else 1 for char in line])
            continue
        matrix = np.array(buffer)
        maybe_fold_a, maybe_fold_b = find_folds(matrix)
        fold_a = maybe_fold_a
        fold_b = maybe_fold_b
        if (fold_a is None) or (fold_b is None):
            maybe_fold_a, maybe_fold_b = find_folds(matrix.T)
            # no type error here because of python boolean short-circuiting:
            # maybe_fold is only None if fold_a is not None, in which case maybe_fold
            # doesn't get evaluated
            fold_a = fold_a or 100 * maybe_fold_a  # type: ignore
            fold_b = fold_b or 100 * maybe_fold_b  # type: ignore
        total_a += fold_a
        total_b += fold_b
        buffer = []

    return total_a, total_b


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    calibration_one, calibration_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{calibration_one=}, {calibration_two=} ({time_us}ms)")
