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
        if sorted_counts == [5]:  # five of a kind
            hand_type_a = 7
            hand_type_b = 7
        elif sorted_counts == [1, 4]:  # four of a kind
            hand_type_a = 6
            if counts["J"] > 0:  # whether we have 1 or 4 Js, upgrade to five of a kind
                hand_type_b = 7
            else:
                hand_type_b = 6
        elif sorted_counts == [2, 3]:  # full house
            hand_type_a = 5
            if counts["J"] > 0:  # whether we have 2 or 3 Js, upgrade to five of a kind
                hand_type_b = 7
            else:
                hand_type_b = 5
        elif sorted_counts == [1, 1, 3]:  # three of a kind
            hand_type_a = 4
            if counts["J"] > 0:  # whether we have 1 or 3 Js, upgrade to four of a kind
                hand_type_b = 6
            else:
                hand_type_b = 4
        elif sorted_counts == [1, 2, 2]:  # two pair
            hand_type_a = 3
            num_j = counts["J"]
            if num_j == 1:  # one J upgrades to full house
                hand_type_b = 5
            elif num_j == 2:  # two Js upgrades to four of a kind
                hand_type_b = 6
            else:
                hand_type_b = 3
        elif sorted_counts == [1, 1, 1, 2]:  # one pair
            hand_type_a = 2
            num_j = counts["J"]
            if num_j > 0:  # whether we have 1 or 2 Jokers, we get three of a kind
                hand_type_b = 4
            else:
                hand_type_b = 2
        else:  # highest card
            hand_type_a = 1
            if counts["J"] == 1:  # if we have 1 J, upgrade to one pair
                hand_type_b = 2
            else:
                hand_type_b = 1
        hand_a = [hand_type_a] + hand_a
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
