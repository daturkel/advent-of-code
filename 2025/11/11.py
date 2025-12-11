import sys
from time import perf_counter

START = "you"
END = "out"

SERVER = "svr"
FFT = "fft"
DAC = "dac"


def get_paths_recursive(
    graph: dict[str, list[str]], start: str, end: str, cache: dict[str, int] = {}
) -> int:
    if start == end:
        return 1
    elif start in cache:
        return cache[start]
    result = 0
    for edge in graph[start]:
        result += get_paths_recursive(graph, edge, end, cache)
    cache[start] = result
    return result


def solve(lines: list[str]) -> tuple[int, int]:
    part_one = 0
    part_two = 0
    graph = {}
    for line in lines:
        head, tail = line.split(": ")
        neighbors = tail.split(" ")
        graph[head] = neighbors
    graph[END] = []
    part_one = get_paths_recursive(graph, START, END, {})

    svr_fft = get_paths_recursive(graph, SERVER, FFT, {})
    svr_dac = get_paths_recursive(graph, SERVER, DAC, {})
    dac_fft = get_paths_recursive(graph, DAC, FFT, {})
    fft_dac = get_paths_recursive(graph, FFT, DAC, {})
    fft_end = get_paths_recursive(graph, FFT, END, {})
    dac_end = get_paths_recursive(graph, DAC, END, {})

    part_two = svr_fft * fft_dac * dac_end + svr_dac * dac_fft * fft_end

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
