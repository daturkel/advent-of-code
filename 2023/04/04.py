import sys
from time import perf_counter


def get_winnings(cards: list[str]) -> tuple[int, int]:
    total = 0
    card_counts = {card_num: 1 for card_num in range(1, len(lines) + 1)}
    for card_idx, line in enumerate(lines, start=1):
        this_card_count = card_counts[card_idx]
        tokens = line.split()
        seperator_index = tokens.index("|")
        winning = set([int(t) for t in tokens[2:seperator_index]])
        ours = [int(t) for t in tokens[seperator_index + 1 :]]
        num_matching = len(winning.intersection(ours))
        if num_matching:
            total += 2 ** (num_matching - 1)
        for forward_idx in range(card_idx + 1, card_idx + 1 + num_matching):
            card_counts[forward_idx] += this_card_count

    return total, sum(card_counts.values())


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.read().splitlines()

    winnings, num_cards = get_winnings(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{winnings=}, {num_cards=} ({time_us}µs)")
