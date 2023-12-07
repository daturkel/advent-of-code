import sys
from collections import Counter
from time import perf_counter

VALUE_MAP = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 10,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
}

NEW_VALUE_MAP = VALUE_MAP | {"J": 0}


def get_hand_type(sorted_counts: list[int]) -> int:
    sorted_hand_types = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 2],
        [1, 2, 2],
        [1, 1, 3],
        [2, 3],
        [1, 4],
        [5],
    ]

    return sorted_hand_types.index(sorted_counts)


def get_winnings(lines: list[str]) -> tuple[int, int]:
    total_a = 0
    total_b = 0
    hands_a = []
    hands_b = []
    for line in lines:
        hand, bet = line.split()
        bet = int(bet)
        counts = Counter(hand)
        sorted_counts = sorted(counts.values())
        hand_a = [VALUE_MAP[char] for char in hand]
        hand_b = [NEW_VALUE_MAP[char] for char in hand]

        hand_type_a = get_hand_type(sorted_counts)
        hand_a = [hand_type_a] + hand_a
        sorted_counts[-1] += counts["J"]  # add number of Js to highest count
        hand_type_b = get_hand_type(sorted_counts)
        hand_b = [hand_type_b] + hand_b
        hands_a.append((hand_a, bet))
        hands_b.append((hand_b, bet))

    sorted_hands_a = sorted(hands_a)
    for rank, (_, bet) in enumerate(sorted_hands_a, start=1):
        total_a += rank * bet

    sorted_hands_b = sorted(hands_b)
    for rank, (_, bet) in enumerate(sorted_hands_b, start=1):
        total_b += rank * bet

    return total_a, total_b


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    winnings, alt_winnings = get_winnings(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{winnings=}, {alt_winnings=} ({time_us}ms)")
