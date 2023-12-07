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


def get_winnings(lines: list[str]) -> tuple[int, int]:
    total = 0
    hands = []
    for line in lines:
        hand, bet = line.split()
        bet = int(bet)
        hand = [VALUE_MAP[char] for char in hand]
        counts = Counter(hand)
        sorted_counts = sorted(counts.values())
        if sorted_counts == [5]:
            hand_type = 7
        elif sorted_counts == [1, 4]:
            hand_type = 6
        elif sorted_counts == [2, 3]:
            hand_type = 5
        elif sorted_counts == [1, 1, 3]:
            hand_type = 4
        elif sorted_counts == [1, 2, 2]:
            hand_type = 3
        elif sorted_counts == [1, 1, 1, 2]:
            hand_type = 2
        else:
            hand_type = 1
        hand = [hand_type] + hand
        hands.append((hand, bet))

    sorted_hands = sorted(hands)
    for rank, (_, bet) in enumerate(sorted_hands, start=1):
        total += rank * bet

    return total, 0


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    winnings, num_cards = get_winnings(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{winnings=}, {num_cards=} ({time_us}µs)")
