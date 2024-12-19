import sys
from time import perf_counter


def is_possible(word: str, tokens: set[str], cache: dict = {}) -> int:
    if word == "":
        return 1
    if word in cache:
        return cache[word]
    possibilities = 0
    for i in range(1, len(word) + 1):
        if word[:i] in tokens:
            possibilities += is_possible(word[i:], tokens)
    cache[word] = possibilities
    return possibilities


def solve(lines: list[str]) -> tuple[int, int]:
    tokens = set(lines[0].split(", "))
    words = lines[2:]
    n_possible = 0
    n_possibilities = 0
    for word in words:
        possibilities = is_possible(word, tokens)
        if possibilities > 0:
            n_possible += 1
        n_possibilities += possibilities
    return n_possible, n_possibilities


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    part_one, part_two = solve(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{part_one=}, {part_two=} ({time_us}ms)")
