#!/usr/bin/env python3

import sys
from time import perf_counter
from typing import Callable


class Monkey:
    def __init__(
        self,
        operation: Callable[[int], int],
        test: Callable[[int], int],
        items: list[int],
    ):
        self.operation = operation
        self.test = test
        self.items = items
        self.inspections = 0

    def inspect_items(self, monkeys: list["Monkey"], lcm: int):
        while self.items:
            self.inspections += 1
            item = self.items.pop(0)
            item = self.operation(item)
            item = item % lcm
            give_to = self.test(item)
            monkeys[give_to].items.append(item)


def parse_monkeys(lines: list[str]) -> tuple[list[Monkey], int]:
    monkeys = []
    lcm = 1

    for line in lines:
        match line.split():
            case ["Starting", "items:", *nums]:
                items_str = f"[{' '.join(nums)}]"
                items = eval(items_str)
            case ["Operation:", *_, op, num]:
                lambda_str = f"lambda old: old {op} {num}"
                operation = eval(lambda_str)  # don't try this at home!
            case ["Test:", *_, num]:
                divisor = int(num)
                # all divisors are prime so the lcm is just their product
                lcm *= divisor
            case ["If", "true:", *_, monkey_num]:
                if_true = monkey_num
            case ["If", "false:", *_, monkey_num]:
                lambda_str = (
                    f"lambda item: {if_true} if item % {divisor} == 0 else {monkey_num}"
                )
                test = eval(lambda_str)
                monkey = Monkey(operation, test, items)
                monkeys.append(monkey)

    return monkeys, lcm


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    with open(input_file, "r") as file:
        lines = [line.strip() for line in file.readlines()]

    tic = perf_counter()

    monkeys, lcm = parse_monkeys(lines)
    for i in range(10000):
        for monkey in monkeys:
            monkey.inspect_items(monkeys, lcm)
    inspections = sorted([monkey.inspections for monkey in monkeys])
    monkey_business = inspections[-1] * inspections[-2]

    toc = perf_counter()
    time_us = round((toc - tic) * 1000)

    print(f"{monkey_business=} ({time_us}ms)")
