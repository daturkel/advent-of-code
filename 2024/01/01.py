import sys
from collections import defaultdict
from time import perf_counter


def get_distance_and_similarity(lines: list[str]) -> tuple[int, int]:
    list_1 = []
    list_2 = []
    counter_1 = defaultdict(int)
    counter_2 = defaultdict(int)
    for line in lines:
        first, second = line.split("   ")
        first = int(first)
        second = int(second)
        list_1.append(first)
        list_2.append(second)
        counter_1[first] += 1
        counter_2[second] += 1
    list_1 = sorted(list_1)
    list_2 = sorted(list_2)
    distance = 0
    for left, right in zip(list_1, list_2):
        distance += abs(left - right)
    similarity = 0
    for key, value in counter_1.items():
        similarity += key * value * counter_2.get(key, 0)
    return distance, similarity


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.readlines()

    distance, similarity = get_distance_and_similarity(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{distance=}, {similarity=} ({time_us}ms)")
